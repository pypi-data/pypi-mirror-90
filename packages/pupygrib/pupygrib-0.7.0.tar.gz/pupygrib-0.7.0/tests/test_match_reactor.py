"""Regression tests for reading match_reactor.grib."""

import datetime

import numpy as np
from pytest import approx

from pupygrib import Message
from pupygrib.edition1 import EndSection, IndicatorSection
from pupygrib.edition1.bds import SimpleGridDataSection
from pupygrib.edition1.bitmap import BitMapSection
from pupygrib.edition1.gds import LatitudeLongitudeGridSection
from pupygrib.edition1.pds import MatchV1ProductSection

PDS = MatchV1ProductSection
GDS = LatitudeLongitudeGridSection
BDS = SimpleGridDataSection
gribfile = "data/match_reactor.grib"


class TestIndicatorSection:
    section_name = "is_"
    fieldnames = {"identifier", "editionNumber", "totalLength"}

    def test_fieldnames(self, section: IndicatorSection) -> None:
        assert section.fieldnames == self.fieldnames

    def test_identifier(self, section: IndicatorSection) -> None:
        assert section.identifier == b"GRIB"

    def test_totalLength(self, section: IndicatorSection) -> None:
        assert section.totalLength == 2834

    def test_editionNumber(self, section: IndicatorSection) -> None:
        assert section.editionNumber == 1


class TestProductDefinitionSection:
    section_name = "pds"
    fieldnames = {
        "section1Length",
        "table2Version",
        "centre",
        "generatingProcessIdentifier",
        "gridDefinition",
        "section1Flags",
        "indicatorOfParameter",
        "indicatorOfTypeOfLevel",
        "level",
        "yearOfCentury",
        "month",
        "day",
        "hour",
        "minute",
        "unitOfTimeRange",
        "P1",
        "P2",
        "timeRangeIndicator",
        "numberIncludedInAverage",
        "numberMissingFromAveragesOrAccumulations",
        "centuryOfReferenceTimeOfData",
        "subCentre",
        "decimalScaleFactor",
        "localDefinitionNumber",
        "generatingProcess",
        "sort",
        "timeRepres",
        "landType",
        "suplScale",
        "molarMass",
        "logTransform",
        "threshold",
        "totalSizeClasses",
        "sizeClassNumber",
        "integerScaleFactor",
        "lowerRange",
        "upperRange",
        "meanSize",
        "STDV",
    }

    def test_fieldnames(self, section: PDS) -> None:
        assert section.fieldnames == self.fieldnames

    def test_section1Length(self, section: PDS) -> None:
        assert section.section1Length == 80

    def test_table2Version(self, section: PDS) -> None:
        assert section.table2Version == 139

    def test_centre(self, section: PDS) -> None:
        assert section.centre == 82

    def test_generatingProcessIdentifier(self, section: PDS) -> None:
        assert section.generatingProcessIdentifier == 1

    def test_gridDefinition(self, section: PDS) -> None:
        assert section.gridDefinition == 255

    def test_section1Flags(self, section: PDS) -> None:
        assert section.section1Flags == 192

    def test_indicatorOfParameter(self, section: PDS) -> None:
        assert section.indicatorOfParameter == 250

    def test_indicatorOfTypeOfLevel(self, section: PDS) -> None:
        assert section.indicatorOfTypeOfLevel == 109

    def test_level(self, section: PDS) -> None:
        assert section.level == 1

    def test_yearOfCentury(self, section: PDS) -> None:
        assert section.yearOfCentury == 16

    def test_month(self, section: PDS) -> None:
        assert section.month == 10

    def test_day(self, section: PDS) -> None:
        assert section.day == 17

    def test_hour(self, section: PDS) -> None:
        assert section.hour == 0

    def test_minute(self, section: PDS) -> None:
        assert section.minute == 0

    def test_unitOfTimeRange(self, section: PDS) -> None:
        assert section.unitOfTimeRange == 1

    def test_P1(self, section: PDS) -> None:
        assert section.P1 == 0

    def test_P2(self, section: PDS) -> None:
        assert section.P2 == 3

    def test_timeRangeIndicator(self, section: PDS) -> None:
        assert section.timeRangeIndicator == 4

    def test_numberIncludedInAverage(self, section: PDS) -> None:
        assert section.numberIncludedInAverage == 1

    def test_numberMissingFromAveragesOrAccumulations(self, section: PDS) -> None:
        assert section.numberMissingFromAveragesOrAccumulations == 0

    def test_centuryOfReferenceTimeOfData(self, section: PDS) -> None:
        assert section.centuryOfReferenceTimeOfData == 21

    def test_subCentre(self, section: PDS) -> None:
        assert section.subCentre == 0

    def test_decimalScaleFactor(self, section: PDS) -> None:
        assert section.decimalScaleFactor == 0

    def test_localDefinitionNumber(self, section: PDS) -> None:
        assert section.localDefinitionNumber == 2

    def test_generatingProcess(self, section: PDS) -> None:
        assert section.generatingProcess == 0

    def test_sort(self, section: PDS) -> None:
        assert section.sort == 3

    def test_timeRepres(self, section: PDS) -> None:
        assert section.timeRepres == 0

    def test_landType(self, section: PDS) -> None:
        assert section.landType == 0

    def test_suplScale(self, section: PDS) -> None:
        assert section.suplScale == 0

    def test_molarMass(self, section: PDS) -> None:
        assert section.molarMass == 13700

    def test_logTransform(self, section: PDS) -> None:
        assert section.logTransform == 1

    def test_threshold(self, section: PDS) -> None:
        assert section.threshold == -999

    def test_totalSizeClasses(self, section: PDS) -> None:
        assert section.totalSizeClasses == 0

    def test_sizeClassNumber(self, section: PDS) -> None:
        assert section.sizeClassNumber == 0

    def test_integerScaleFactor(self, section: PDS) -> None:
        assert section.integerScaleFactor == 0

    def test_lowerRange(self, section: PDS) -> None:
        assert section.lowerRange == 0

    def test_upperRange(self, section: PDS) -> None:
        assert section.upperRange == 0

    def test_meanSize(self, section: PDS) -> None:
        assert section.meanSize == 0

    def test_STDV(self, section: PDS) -> None:
        assert section.STDV == 0


class TestGridDescriptionSection:
    section_name = "gds"
    fieldnames = {
        "section2Length",
        "numberOfVerticalCoordinateValues",
        "pvlLocation",
        "dataRepresentationType",
        "Ni",
        "Nj",
        "latitudeOfFirstGridPoint",
        "longitudeOfFirstGridPoint",
        "resolutionAndComponentFlags",
        "latitudeOfLastGridPoint",
        "longitudeOfLastGridPoint",
        "iDirectionIncrement",
        "jDirectionIncrement",
        "scanningMode",
    }

    def test_fieldnames(self, section: GDS) -> None:
        assert section.fieldnames == self.fieldnames

    def test_section2Length(self, section: GDS) -> None:
        assert section.section2Length == 1130

    def test_numberOfVerticalCoordinateValues(self, section: GDS) -> None:
        assert section.numberOfVerticalCoordinateValues == 5

    def test_pvlLocation(self, section: GDS) -> None:
        assert section.pvlLocation == 35

    def test_dataRepresentationType(self, section: GDS) -> None:
        assert section.dataRepresentationType == 0

    def test_Ni(self, section: GDS) -> None:
        assert section.Ni == 117

    def test_Nj(self, section: GDS) -> None:
        assert section.Nj == 103

    def test_latitudeOfFirstGridPoint(self, section: GDS) -> None:
        assert section.latitudeOfFirstGridPoint == 17250

    def test_longitudeOfFirstGridPoint(self, section: GDS) -> None:
        assert section.longitudeOfFirstGridPoint == 30250

    def test_resolutionAndComponentFlags(self, section: GDS) -> None:
        assert section.resolutionAndComponentFlags == 128

    def test_latitudeOfLastGridPoint(self, section: GDS) -> None:
        assert section.latitudeOfLastGridPoint == 42750

    def test_longitudeOfLastGridPoint(self, section: GDS) -> None:
        assert section.longitudeOfLastGridPoint == 59250

    def test_iDirectionIncrement(self, section: GDS) -> None:
        assert section.iDirectionIncrement == 250

    def test_jDirectionIncrement(self, section: GDS) -> None:
        assert section.jDirectionIncrement == 250

    def test_scanningMode(self, section: GDS) -> None:
        assert section.scanningMode == 64


class TestBitMapSection:
    section_name = "bitmap"
    fieldnames = {
        "section3Length",
        "numberOfUnusedBitsAtEndOfSection3",
        "tableReference",
        "bitmap",
    }

    def test_fieldnames(self, section: BitMapSection) -> None:
        assert section.fieldnames == self.fieldnames

    def test_section3Length(self, section: BitMapSection) -> None:
        assert section.section3Length == 1513

    def test_numberOfUnusedBitsAtEndOfSection3(self, section: BitMapSection) -> None:
        assert section.numberOfUnusedBitsAtEndOfSection3 == 5

    def test_tableReference(self, section: BitMapSection) -> None:
        assert section.tableReference == 0

    def test_bitmap(self, section: BitMapSection) -> None:
        bitmap = section.bitmap
        assert len(bitmap) == 1507 * 8 - 5
        assert bitmap.sum() == 44


class TestBinaryDataSection:
    section_name = "bds"
    fieldnames = {
        "section4Length",
        "dataFlag",
        "binaryScaleFactor",
        "referenceValue",
        "bitsPerValue",
        "values",
    }

    def test_fieldnames(self, section: BDS) -> None:
        assert section.fieldnames == self.fieldnames

    def test_section4Length(self, section: BDS) -> None:
        assert section.section4Length == 99

    def test_dataFlag(self, section: BDS) -> None:
        assert section.dataFlag == 0

    def test_binaryScaleFactor(self, section: BDS) -> None:
        assert section.binaryScaleFactor == -9

    def test_referenceValue(self, section: BDS) -> None:
        assert section.referenceValue == approx(-84.7472)

    def test_bitsPerValue(self, section: BDS) -> None:
        assert section.bitsPerValue == 16

    def test_values(self, section: BDS) -> None:
        assert len(section.values) == 44


class TestEndSection:
    section_name = "end"
    fieldnames = {"endOfMessage"}

    def test_fieldnames(self, section: EndSection) -> None:
        assert section.fieldnames == self.fieldnames

    def test_endOfMessage(self, section: EndSection) -> None:
        assert section.endOfMessage == b"7777"


class TestMessage:
    def test_time(self, message: Message) -> None:
        assert message.get_time() == datetime.datetime(2016, 10, 17, 0, 0)

    def test_longitudes(self, message: Message, target_longitudes: np.ndarray) -> None:
        longitudes, _ = message.get_coordinates()
        np.testing.assert_allclose(longitudes, target_longitudes)

    def test_latitudes(self, message: Message, target_latitudes: np.ndarray) -> None:
        _, latitudes = message.get_coordinates()
        np.testing.assert_allclose(latitudes, target_latitudes)

    def test_values(self, message: Message, target_values: np.ndarray) -> None:
        values = message.get_values()
        np.testing.assert_allclose(values.filled(0), target_values)
