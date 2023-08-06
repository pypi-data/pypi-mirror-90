import logging
import datetime
import os
import struct
from obspy import UTCDateTime
import numpy as np
from math import floor
from math import ceil
from numbers import Number


def tup2time(fraction, seconds):
    # logs = logging.getLogger('tup2time')
    # logs.debug('seconds: %s' % seconds)
    # logs.debug('fraction: %s' % fraction)

    dt1904 = datetime.datetime(1904, 1, 1)
    delta = seconds + fraction * 2**(-64)
    result = dt1904 + datetime.timedelta(seconds=delta)
    # logs.debug('Date-time %s' % result)
    return result


class PotentialGap(Exception):
    pass


class NoData(Exception):
    pass


class TDMS(object):
    """Class to read and export seismic waveforms in TDMS format"""

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Method which close open resources after using the syntax 'with object:' and use it inside"""
        if self.__fi is not None:
            self.__fi.close()

    def __enter__(self):
        """Method which allows to use the syntax 'with object:' and use it inside"""

        # Create a buffer space to store the signal coefficients to be
        # convoluted during the decimation
        # for channel in range(self.__chstart, self.__chstop + 1, self.__chstep):
        for channel in self.__channels:
            logging.debug('Create empty buffer for channel %s' % channel)
            self.__buffer[channel] = None

        return self

    def __init__(self, filename, directory='.', chstart=0, chstop=None, chstep=1, channels=None,
                 starttime=None, endtime=None, iterate='D', decimate=1, firfilter='fir235',
                 loglevel='INFO'):
        """Initialize the TDMS object selecting the data, channels and decimation

        :param filename: Experiment to read and process. Usually the first part of the filenames
        :type filename: str
        :param directory: Directory where files are located
        :type directory: str
        :param chstart: First channel to select
        :type chstart: int
        :param chstop: Last channel to select
        :type chstop: int
        :param chstep: Step between channels in the selection
        :type chstep: int
        :param channels: Selection of channels to work with (list of integers)
        :type channels: list or NoneType
        :param starttime: Start of the selected time window
        :type starttime: datetime.datetime or NoneType
        :param endtime: End of the selected time window
        :type endtime: datetime.datetime or NoneType
        :param iterate: Select either Data (D) or Metadata (M)
        :type iterate: str
        :param decimate: Factor by which the sampling rate is lowered by decimation
        :type decimate: int
        :param firfilter: Filter to apply in case of decimation (fir235 is the only option)
        :type firfilter: str
        :param loglevel: Verbosity in the output
        :type loglevel: str
        """

        # Log level
        self.__loglevel = loglevel
        logs = logging.getLogger('Init TDMS')
        logs.setLevel(loglevel)

        project_dir = os.path.dirname(__file__)

        # Decimation factor
        self.__decimate = decimate

        # Selection of channels
        if not isinstance(chstart, Number) or not isinstance(chstep, Number):
            logs.error('chstart and chstep must be numbers and preferably ints')
            raise TypeError('chstart and chstep must be numbers and preferably ints')

        if not isinstance(chstop, Number) and chstop is not None:
            logs.error('chstop must be a number or None')
            raise TypeError('chstop must be a number or None')

        if not isinstance(channels, list) and channels is not None:
            logs.error('channels must be a list of numbers or None')
            raise TypeError('channels must be a list of numbers or None')

        self.__chstart = chstart
        self.__chstop = chstop
        self.__chstep = chstep

        # channels has priority. Otherwise, chstart, chstop and chstep are used
        if channels is not None and isinstance(channels, list):
            self.__channels = channels
            # List of channels cannot be empty
            if not len(self.__channels):
                raise Exception('Channel list is empty!')

        else:
            # If chstart, chstop and chstep will define the selected channels we need to keep the three
            #  values (start, stop, step) and define the channels later in readmetadata
            self.__channels = None
            # self.__channels = list(range(chstart, chstop+1, chstep))

        # Time window selection
        self.__twstart = starttime
        self.__twend = endtime

        # Available time window
        self.starttime = None
        self.endtime = None

        # Sampling Rate
        self.sampling_rate = None

        # File currently being processed
        self.__currentfile = None

        # Name of file
        self.__filename = filename
        self.__directory = directory

        # List of available files in the directory
        self.__available = list()

        for file in sorted(os.listdir(directory)):
            if not file.startswith(filename):
                continue

            dt = datetime.datetime.strptime(file[len(filename):-len('.tdms')], '_%Z_%Y%m%d_%H%M%S.%f')
            self.__available.append({'dt': dt, 'name': file, 'samples': None})
            if self.__twstart is None:
                self.__twstart = dt

        # Set the time window selection to the minimum datetime found
        if self.__twstart < self.__available[0]['dt']:
            self.__twstart = self.__available[0]['dt']

        # Keep the values in case we need to reset them
        self.__origstarttime = self.__twstart
        self.__origendtime = self.__twend

        # What should we iterate? D: Data; M: Metadata
        self.iterate = iterate

        # Define a buffer to store the window over the signal to be
        # convoluted with the FIR filter wile decimating
        # Keys will be channel number and the values will be np.arrays
        self.__buffer = dict()

        # Datatype of each channel
        self.__datatypes = dict()

        # Dictionary to save the metadata defined in the file
        self.metadata = dict()

        # Initialization of local variables
        self.__HEADERLEN = 28
        self.__MAXSAMPLES = 30000
        self.__FF64b = 0xFFFFFFFFFFFFFFFF
        self.__FF32b = 0xFFFFFFFF

        self.__data2mask = {
            0: ('c', 1),  # tdsTypeVoid
            1: ('b', 1),  # tdsTypeI8
            2: ('h', 2),  # tdsTypeI16
            3: ('i', 4),  # tdsTypeI32
            4: ('q', 8),  # tdsTypeI64
            5: ('b', 1),  # tdsTypeU8
            6: ('h', 2),  # tdsTypeU16
            7: ('i', 4),  # tdsTypeU32
            8: ('q', 8),  # tdsTypeU64
            9: ('f', 4),  # tdsTypeSingleFloat
            10: ('d', 8),  # tdsTypeDoubleFloat
            0x20: ('I', 4),  # tdsTypeString
            0x21: ('?', 1),  # tdsTypeBoolean
            0x44: ('Qq', 16)  # tdsTypeTimeStamp
        }

        # Read filter to decimate
        auxfilter = list()
        with open(os.path.join(project_dir, 'data/filters/%s.txt' % firfilter)) as fin:
            for line in fin.readlines():
                auxfilter.append(float(line))

        self.__filter = np.array(auxfilter)
        logs.debug('FIR filter: %s' % self.__filter)
        #     tdsTypeFixedPoint = 0x4F,
        #     tdsTypeComplexSingleFloat = 0x08000c,
        #     tdsTypeComplexDoubleFloat = 0x10000d,
        #     tdsTypeDAQmxRawData = 0xFFFFFFFF

        # Other variables to be read from the headers
        self.__hasInterleavedData = None
        self.__endian = None
        self.__datatype = None
        self.__datatypesize = None
        self.numchannels = None
        self.__samples = None
        self.__samplestart = None
        self.__sampleend = None
        self.__samplecur = None

        try:
            self.__search_data()
        except IndexError:
            raise NoData()

    def __select_file(self):
        logs = logging.getLogger('Select file')
        logs.setLevel(self.__loglevel)

        # print('select', self.__twstart, self.starttime, self.__currentfile)

        if self.__currentfile is None:
            for idx, fi in enumerate(self.__available):
                # print(self.__twstart, fi['dt'])
                if self.__twstart < fi['dt']:
                    if not idx:
                        raise Exception('Data not available in the specified time window')
                    filename = os.path.join(self.__directory, self.__available[idx-1]['name'])
                    self.__currentfile = idx-1
                    # print(self.__currentfile, filename)
                    logs.debug(
                        'Opening %s; Starttime: %s' % (self.__available[self.__currentfile]['name'], self.__twstart))
                    break
            else:
                raise Exception('Data not available in the specified time window')
        elif self.__currentfile >= len(self.__available):
            logs.debug('Last file already processed')
            # No more data to iterate
            raise IndexError
        else:
            filename = os.path.join(self.__directory, self.__available[self.__currentfile]['name'])
            self.__twstart = self.__available[self.__currentfile]['dt']
            if (self.__twend is not None) and (self.__twstart > self.__twend):
                logs.debug('Start is greater than end. %s %s' % (self.__twstart, self.__twend))
                raise IndexError
            logs.debug('Opening %s; Starttime: %s' % (self.__available[self.__currentfile]['name'], self.__twstart))

        # print(self.__twstart)
        # Reset some properties before opening the new file
        self.starttime = self.__available[self.__currentfile]['dt']
        # print(self.starttime)
        self.endtime = None
        self.metadata = dict()

        # Save the handle of the open file to be processed
        self.__fi = open(filename, 'rb')

        # Read headers
        leadin = self.__fi.read(self.__HEADERLEN)
        (tag, ToCmask) = struct.unpack('<4si', leadin[:8])

        ktocmetadata = 1 << 1
        ktocnewobjlist = 1 << 2
        ktocrawdata = 1 << 3
        ktocinterleaveddata = 1 << 5
        ktocbigendian = 1 << 6
        ktocdaqmxrawdata = 1 << 7

        hasmetadata = bool(ToCmask & ktocmetadata)
        hasnewobjects = bool(ToCmask & ktocnewobjlist)
        hasrawdata = bool(ToCmask & ktocrawdata)
        self.__hasInterleavedData = bool(ToCmask & ktocinterleaveddata)
        hasdaqmxrawdata = bool(ToCmask & ktocdaqmxrawdata)

        # All input from now on will be formatted by this
        self.__endian = '>' if ToCmask & ktocbigendian else '<'

        if tag.decode() != 'TDSm':
            raise Exception('Tag is not TDSm!')

        (versionTDMS, self.__segmentOffset, self.__dataOffset) = \
            struct.unpack('%ciQQ' % self.__endian, leadin[8:])

        logs.debug((tag, ToCmask, versionTDMS, self.__segmentOffset, self.__dataOffset))

        if versionTDMS != 4713:
            logs.warning('Version number is not 4713!')

        if self.__segmentOffset == self.__FF64b:
            logs.error('Severe problem while writing data (crash, power outage)')

        if hasmetadata and not self.__dataOffset:
            logs.error('Flag indicates Metadata but its length is 0!')

        if hasdaqmxrawdata:
            logs.warning('DAQmx raw data is still not supported!')

        # Absolute offsets
        self.__segmentOffset += self.__HEADERLEN
        self.__dataOffset += self.__HEADERLEN

        logs.debug('Metadata: ' + ('yes' if hasmetadata else 'no'))
        logs.debug('Object list: ' + ('yes' if hasnewobjects else 'no'))
        logs.debug('Raw data: ' + ('yes' if hasrawdata else 'no'))
        logs.debug('Interleaved data: ' + ('yes' if self.__hasInterleavedData else 'no'))
        logs.debug('BigEndian: ' + ('yes' if self.__endian == '<' else 'no'))
        logs.debug('DAQmx raw data: ' + ('yes' if hasdaqmxrawdata else 'no'))

        # self.__readmetadata()

    def __search_data(self):
        """
        :raise: IndexError
        """

        while True:
            # Loop through files until there is nothing else (IndexError)
            self.__select_file()

            # Read the metadata and calculate samples to read
            # Skip to the next file if there is a gap
            try:
                self.__readmetadata()
                return
            except PotentialGap:
                logging.debug('Potential gap detected!')
                self.__currentfile += 1

    # Rename to make it accessible to users
    def reset(self):
        self.__twstart = self.__origstarttime
        self.__twend = self.__origendtime
        self.__currentfile = None
        self.__search_data()

    def __readmetadata(self):
        # Metadata
        logs = logging.getLogger('Read Metadata')
        # handler = logging.StreamHandler(sys.stdout)
        # logs.addHandler(handler)
        self.__fi.seek(self.__HEADERLEN, 0)

        # Number of objects (unsigned int - 32b)
        numobjects = struct.unpack('%cI' % self.__endian, self.__fi.read(4))[0]
        logs.debug('Number of objects in metadata: %s' % numobjects)

        curstarttime = None
        datatype = None
        numchannels = 0
        # chunkSize = 0
        for obj in range(numobjects):
            # channelSize = 0
            objpath = self.__readstring()
            # logs.debug('Object %s: %s' % (obj, objPath))

            self.metadata[obj] = {'path': objpath}

            rawdataidx = struct.unpack('%cI' % self.__endian, self.__fi.read(4))[0]

            if rawdataidx == self.__FF32b:
                logs.debug('No raw data assigned to segment %s' % obj)
                self.metadata[obj]['data'] = False
                self.__readproperties(self.metadata[obj])

                try:
                    if self.sampling_rate is None:
                        self.sampling_rate = self.metadata[obj]['SamplingFrequency[Hz]']
                except KeyError:
                    pass

                try:
                    curstarttime = self.metadata[obj]['GPSTimeStamp']
                    if self.starttime is None:
                        self.starttime = self.metadata[obj]['GPSTimeStamp']
                except KeyError:
                    pass

                continue

            elif not rawdataidx:
                logs.debug('Raw data index in this segment matches the index the same object had in the previous '
                           'segment')

            else:
                self.metadata[obj]['data'] = True
                self.metadata[obj]['id'] = numchannels
                numchannels += 1

                # There is raw data!
                # sizeBytes = None
                datatype, arraylen, numvalues = struct.unpack('%cIIQ' % self.__endian, self.__fi.read(16))
                if datatype == 0x20:
                    self.metadata[obj]['sizeBytes'] = struct.unpack('%cQ' % self.__endian, self.__fi.read(8))[0]

                if arraylen != 1:
                    logs.error('Array length MUST be 1! Actual value: %s' % arraylen)

                self.metadata[obj]['datatype'] = self.__data2mask[datatype][0]
                self.metadata[obj]['sampling_rate'] = self.sampling_rate
                self.metadata[obj]['starttime'] = curstarttime

                self.__readproperties(self.metadata[obj])

        # Set the data type as numpy expects it
        if datatype is None:
            raise Exception('datatype definition not found in any channel!')

        if self.__data2mask[datatype][0] == 'h':
            self.__datatype = '%ci2' % self.__endian
        elif self.__data2mask[datatype][0] == 'f':
            self.__datatype = '%cf4' % self.__endian
        else:
            raise Exception('Data type not supported! (%s)' % self.__data2mask[datatype][0])

        self.__datatypesize = self.__data2mask[datatype][1]
        self.numchannels = numchannels

        # If channels was not defined at creation time
        if self.__channels is None:
            if self.__chstart >= numchannels:
                raise Exception('No valid channel IDs selected!')
            if self.__chstop is None or self.__chstop >= numchannels:
                logs.info('Resetting chstop from %s to %s' % (self.__chstop, numchannels-1))
                self.__chstop = numchannels - 1
            # Define list of selected channels
            self.__channels = list(range(self.__chstart, self.__chstop + 1, self.__chstep))

        self.__samples = int((self.__segmentOffset - self.__dataOffset) / numchannels / self.__datatypesize)

        # Calculate endtime based on the number of samples declared and the sampling rate
        self.endtime = self.starttime + datetime.timedelta(seconds=(self.__samples-1)/self.sampling_rate)
        for obj in self.metadata:
            if not self.metadata[obj]['data']:
                continue

            self.metadata[obj]['samples'] = self.__samples
            self.metadata[obj]['endtime'] = curstarttime + \
                datetime.timedelta(seconds=(self.__samples - 1) / self.sampling_rate)

        # Sample to start extraction from based on the initial datetime of the file (__twstart)
        # print(self.__twstart, self.starttime)
        self.__samplestart = max(floor((self.__twstart - self.starttime).total_seconds() * self.sampling_rate), 0)
        if self.__samplestart >= self.__samples:
            raise PotentialGap('Start reading at %s, but only %s samples' % (self.__samplestart, self.__samples))

        # Should I readjust __twstart to align it exactly with the time of the samples?
        # print(self.__twstart, self.starttime + datetime.timedelta(seconds=self.__samplestart/self.sampling_rate))
        self.__twstart = self.starttime + datetime.timedelta(seconds=self.__samplestart/self.sampling_rate)
        # print(self.__twstart, self.starttime, self.__samplestart)

        self.__samplecur = self.__samplestart

        # Open end or beyond this file: read until the last sample
        if (self.__twend is None) or (self.__twend >= self.endtime):
            self.__sampleend = self.__samples-1
        else:
            # Otherwise calculate which one is the last sample to read
            self.__sampleend = ceil((self.__twend - self.starttime).total_seconds() * self.sampling_rate)
            # print(self.__twend, self.starttime, (self.__twend - self.starttime).total_seconds(), self.__sampleend)

        logs.debug('Samples: %s' % self.__samples)
        logs.debug('Samples selected: %s-%s' % (self.__samplestart, self.__sampleend))
        logs.debug('Total chunks size: %s' % (self.__segmentOffset - self.__dataOffset))
        channellength = ((self.__segmentOffset - self.__dataOffset)/numchannels/self.__data2mask[datatype][1])
        logs.debug('Length of channel: %d' % channellength)

        # New or changed objects
        # newobjects = struct.unpack('%cI' % self.__endian, self.__fi.read(4))[0]

    def __iter__(self):
        """Iterate through data (or metadata) and filter and decimate if requested"""

        # Create logger
        logs = logging.getLogger('__iter__')

        if self.iterate == 'M':
            for info in self.__iter_metadata__():
                yield info

        else:
            # In the case that we iterate to get data
            # If no decimation is needed
            if self.__decimate == 1:
                for info in self.__iter_data__():
                    yield info
            else:
                # Use an input buffer to store the data coming in chunks from __iter_data__
                inbuf = dict()
                # Keep values in a buffer before returning them to be packed in miniSEED records
                # Otherwise, the chunks could be too short and the final size of the mSEED
                # would be too large
                outbuf = dict()
                # Keep filtered values which should be later decimated
                nodecimation = dict()
                # Time of the first sample in the next file
                expectedtime = dict()
                # Flag to know if we are at the beginning of the chunk
                startofchunk = True

                for data, stats in self.__iter_data__():
                    ch = int(stats['station'])

                    # Check expected time for each channel
                    if ch in expectedtime:
                        if expectedtime[ch] != stats['starttime']:
                            logs.warning('GAP! Expected: %s ; Current: %s' % (expectedtime[ch], stats['starttime']))
                            # Gap!
                            if ch in inbuf:
                                logs.debug('Remove last %s components of previous chunk' % len(inbuf[ch]['data']))
                                del inbuf[ch]

                            # Flush outbuf?
                            if ch in outbuf:
                                leftover = len(nodecimation[ch]) % 5
                                # outbuf[ch]['stats']['starttime'] += 1/outbuf[ch]['stats']['sampling_rate']
                                outbuf[ch]['stats']['npts'] = 1
                                yield nodecimation[ch][-leftover::5], outbuf[ch]['stats']
                                logs.debug('Flushing: %s %s' % (nodecimation[ch][-leftover::5], outbuf[ch]['stats']))
                                del outbuf[ch]
                            # self.__buffer[ch] = None
                            del expectedtime[ch]
                            # Start the processing of a new chunk after the gap
                            startofchunk = True

                    expectedtime[ch] = stats['starttime'] + stats['npts']/self.sampling_rate

                    # Store values coming from __iter_data__
                    if ch not in inbuf:
                        # Initialize an idx and array with the first chunk of data
                        inbuf[ch] = {'data': np.array(data),
                                     'stats': stats}
                        # print('inbuf: %s' % inbuf[ch]['stats'])
                    else:
                        inbuf[ch]['data'] = np.append(inbuf[ch]['data'], data)

                    # Store values resulting from the convolution
                    if ch not in outbuf:
                        # Initialize an idx and array with the first chunk of data
                        outbuf[ch] = {'stats': inbuf[ch]['stats'].copy()}

                        # Modify the starting time only if it is the beginning of the signal
                        if startofchunk:
                            outbuf[ch]['stats']['starttime'] += (len(self.__filter)-1)/(2 * outbuf[ch]['stats']['sampling_rate'])
                            startofchunk = False

                        # Change the headers to reflect the decimation
                        outbuf[ch]['stats']['sampling_rate'] = stats['sampling_rate']/5
                        # print('outbuf new: %s' % outbuf[ch]['stats'])

                    # If there are not enough components move to the next chunk
                    if len(inbuf[ch]['data']) < len(self.__filter):
                        continue

                    # Convolution of inbuf with filter and then leave the last 234 values (len(filter)-1)
                    # This convolution is performed on a long array (inbuf) and a default filter with 235 components
                    nodecimation[ch] = np.convolve(inbuf[ch]['data'], self.__filter, 'valid').astype(data.dtype)
                    logs.debug('filtered: %d components' % len(nodecimation[ch]))
                    logs.debug('filtered[%d][:11] %s' % (ch, nodecimation[ch][:11]))
                    logs.debug('filtered[%d][-11:] %s' % (ch, nodecimation[ch][-11:]))

                    # Check if we can copy as many components as a multiple of the decimation factor
                    leftover = len(nodecimation[ch]) % 5
                    logs.debug('filtered: leave %d components for next iteration %s' % (leftover, nodecimation[ch][-leftover:]))
                    if leftover:
                        if 'data' not in outbuf[ch]:
                            outbuf[ch]['data'] = nodecimation[ch][:-leftover][::5]
                        else:
                            outbuf[ch]['data'] = np.append(outbuf[ch]['data'], nodecimation[ch][:-leftover][::5])
                    else:
                        if 'data' not in outbuf[ch]:
                            outbuf[ch]['data'] = nodecimation[ch][::5]
                        else:
                            outbuf[ch]['data'] = np.append(outbuf[ch]['data'], nodecimation[ch][::5])

                    logs.debug('outbuf[%d][:11] %s' % (ch, outbuf[ch]['data'][:11]))
                    logs.debug('outbuf[%d][-11:] %s' % (ch, outbuf[ch]['data'][-11:]))

                    # Keep values which will be needed to start again in the next file
                    # to avoid boundary effects. leftover comes from the extra values we already calculated
                    # but we could not use because of decimation. Therefore, we will put them in the beginning
                    # and calculate again
                    valuesprocessed = len(inbuf[ch]['data']) - len(self.__filter) + 1 - leftover
                    logs.debug('values processed: %d' % valuesprocessed)
                    inbuf[ch]['data'] = inbuf[ch]['data'][-len(self.__filter)+1-leftover:]
                    inbuf[ch]['stats']['starttime'] += valuesprocessed / inbuf[ch]['stats']['sampling_rate']

                    # If there is enough data
                    if len(outbuf[ch]['data']) > 2000:
                        outbuf[ch]['stats']['npts'] = len(outbuf[ch]['data'])
                        # print('outbuf: %s npts' % outbuf[ch]['index'])
                        yield outbuf[ch]['data'], outbuf[ch]['stats']
                        # Reset outbuf with an empty array and the next starttime (in headers)
                        outbuf[ch]['stats']['starttime'] += len(outbuf[ch]['data']) / outbuf[ch]['stats']['sampling_rate']
                        del outbuf[ch]['data']

                # Do I need here to flush all remaining components from outbuf?
                for ch in outbuf:
                    if ('data' in outbuf[ch]) and len(outbuf[ch]['data']):
                        outbuf[ch]['stats']['npts'] = len(outbuf[ch]['data'])
                        yield outbuf[ch]['data'], outbuf[ch]['stats']

    def __iter_data__(self):
        """Read data from files based on channel selection"""
        # Data
        logs = logging.getLogger('Iterate Data')

        while (self.__twend is None) or (self.__twstart < self.__twend):
            data = self.__readdata(channels=self.__channels)
            # Loop through channels
            for ch in self.__channels:
                stats = {'network': 'XX', 'station': '%05d' % ch, 'location': '',
                         'channel': 'FH1', 'npts': len(data[ch]),
                         'sampling_rate': self.sampling_rate,
                         'starttime': UTCDateTime(self.__twstart),
                         'mseed': {'byteorder': self.__endian,
                                   'dataquality': 'D',
                                   'record_length': 512}}
                logs.debug('Data length: %d; First component: %s' % (len(data[ch]), data[ch][0]))
                yield data[ch], stats

            # No more data in this file. Skip to the next one.
            self.__currentfile += 1
            try:
                logs.debug('Moving to next file...')
                self.__search_data()
            except IndexError:
                break

    def __iter_metadata__(self):
        # Metadata
        # logs = logging.getLogger('Iterate Metadata')

        # channels = list(range(self.__chstart, self.__chstop+1, self.__chstep))

        while (self.__twend is None) or (self.__twstart < self.__twend):
            for obj in self.metadata:
                # if 'id' in self.metadata[obj] and self.metadata[obj]['id'] not in channels:
                if 'id' in self.metadata[obj] and self.metadata[obj]['id'] not in self.__channels:
                    continue
                yield self.metadata[obj]

            # No more data in this file. Skip to the next one.
            self.__currentfile += 1
            try:
                self.__search_data()
            except IndexError:
                break

    def __readstring(self):
        """All strings in TDMS files, such as object paths, property names, property values, and raw data values,
        are encoded in UTF-8 Unicode. All of them, except for raw data values, are preceded by a 32-bit unsigned
        integer that contains the length of the string in bytes, not including the length value itself. Strings in
        TDMS files can be null-terminated, but since the length information is stored, the null terminator will be
        ignored when you read from the file.
        """
        # logs = logging.getLogger('readstring')
        strlen = struct.unpack('%cI' % self.__endian, self.__fi.read(4))
        # logs.debug('String of length %s' % strlen)
        return self.__fi.read(strlen[0]).decode()

    def __readvalue(self):
        # logs = logging.getLogger('readvalue')

        datatype = self.__readdatatype()
        # logs.debug('datatype: 0x%x' % datatype)

        # Consider cases which need another read
        # 0x20 is a string. Read again!
        if datatype == 0x20:
            return self.__readstring()

        (mask, numBytes) = self.__data2mask[datatype]
        # logs.debug('Mask: %s; Bytes: %s' % (mask, numBytes))
        # This instruction returns a tuple. Needed for timestamps
        result = struct.unpack('%c%s' % (self.__endian, mask), self.__fi.read(numBytes))

        # 0x44 is a timestamp. Read again!
        if datatype == 0x44:
            result = tup2time(*result)
        else:
            # Disassemble the tuple if not a timestamp
            result = result[0]

        # logs.debug('result: %s' % result)
        return result

    def __readproperties(self, result=None):
        """For each property, the following information is stored:
            Name (string)
            Data type (tdsDataType)
            Value (numerics stored binary, strings stored as explained above).
        """
        logs = logging.getLogger('readproperties')

        if result is None:
            result = dict()

        numprops = struct.unpack('%cI' % self.__endian, self.__fi.read(4))[0]
        if numprops:
            logs.debug('%s properties' % numprops)

        for prop in range(numprops):
            propstr = self.__readstring()
            value = self.__readvalue()
            result[propstr] = value
            if self.iterate == 'M':
                logs.debug('%s: %s' % (propstr, value))

        return result

    def __readdatatype(self):
        return struct.unpack('%cI' % self.__endian, self.__fi.read(4))[0]

    def __readdata(self, channels=None):
        """Read a chunk of data from the specified channels.
        Update the attribute __samplecur

        :param channels: List of channel numbers to read data from
        :type channels: list
        :return: Dictionary with channel as key and a numpy array with data as value
        :rtype: dict
        """

        logs = logging.getLogger('Read data')
        logs.setLevel(self.__loglevel)

        # If there is no channel specified read from all selected channels
        if channels is None:
            channels = self.__channels
        else:
            for ch in channels:
                # All channels must be within the originally selected channels
                if ch not in self.__channels:
                    logs.error('Trying to read data from an unselected channel!')
                    raise Exception('Trying to read data from an unselected channel!')

        result = dict()

        numsamples = self.__sampleend - self.__samplestart + 1
        # numSamples = min(self.__sampleend - self.__samplecur + 1, self.__MAXSAMPLES)
        if not self.__hasInterleavedData:
            for ch in channels:
                # Seek where the channel starts and add the offset to the first
                # sample to read based in the time window selection
                # self.__fi.seek(self.__dataOffset + self.__datatypesize*self.__samples*channel + self.__samplestart, 0)
                self.__fi.seek(self.__dataOffset + self.__datatypesize*self.__samples*ch + self.__samplecur, 0)

                # Read all selected data from the channel in one step
                result[ch] = np.fromfile(self.__fi, dtype=self.__datatype, count=numsamples)

            # Update the current sample number based on the number of components read
            self.__samplecur += numsamples

            return result

        # Seek where the raw data starts and add the offset to the first
        # sample to read based in the time window selection
        # self.__fi.seek(self.__dataOffset + self.__samplestart*self.__datatypesize*self.numchannels, 0)
        self.__fi.seek(self.__dataOffset + self.__samplecur*self.__datatypesize*self.numchannels, 0)

        # Reserve the data for the result
        for ch in channels:
            result[ch] = np.zeros((numsamples,), dtype=self.__datatype)

        for sample in range(numsamples):
            # Read from all channels and select the specific one with an index (channel)
            allchannels = np.fromfile(self.__fi, dtype=self.__datatype, count=self.numchannels)
            for ch in channels:
                result[ch][sample] = allchannels[ch]

        # Update the current sample number based on the number of components read
        self.__samplecur += numsamples

        return result
