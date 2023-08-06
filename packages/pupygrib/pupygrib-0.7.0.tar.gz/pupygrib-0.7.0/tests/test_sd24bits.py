"""Regression tests for reading sd24bits.grib."""

import numpy as np

from pupygrib.edition1 import EndSection, IndicatorSection
from pupygrib.edition1.bds import SimpleGridDataSection
from pupygrib.edition1.gds import LatitudeLongitudeGridSection
from pupygrib.edition1.pds import ProductDefinitionSection

PDS = ProductDefinitionSection
GDS = LatitudeLongitudeGridSection
BDS = SimpleGridDataSection
gribfile = "data/sd24bits.grib"


class TestIndicatorSection:
    section_name = "is_"
    fieldnames = {"identifier", "editionNumber", "totalLength"}

    def test_fieldnames(self, section: IndicatorSection) -> None:
        assert section.fieldnames == self.fieldnames

    def test_identifier(self, section: IndicatorSection) -> None:
        assert section.identifier == b"GRIB"

    def test_totalLength(self, section: IndicatorSection) -> None:
        assert section.totalLength == 6804

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
        "localDefinitionNumber",
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
    }

    def test_fieldnames(self, section: PDS) -> None:
        assert section.fieldnames == self.fieldnames

    def test_section1Length(self, section: PDS) -> None:
        assert section.section1Length == 52

    def test_table2Version(self, section: PDS) -> None:
        assert section.table2Version == 128

    def test_centre(self, section: PDS) -> None:
        assert section.centre == 98

    def test_generatingProcessIdentifier(self, section: PDS) -> None:
        assert section.generatingProcessIdentifier == 255

    def test_gridDefinition(self, section: PDS) -> None:
        assert section.gridDefinition == 255

    def test_section1Flags(self, section: PDS) -> None:
        assert section.section1Flags == 128

    def test_indicatorOfParameter(self, section: PDS) -> None:
        assert section.indicatorOfParameter == 141

    def test_indicatorOfTypeOfLevel(self, section: PDS) -> None:
        assert section.indicatorOfTypeOfLevel == 1

    def test_level(self, section: PDS) -> None:
        assert section.level == 0

    def test_yearOfCentury(self, section: PDS) -> None:
        assert section.yearOfCentury == 79

    def test_month(self, section: PDS) -> None:
        assert section.month == 12

    def test_day(self, section: PDS) -> None:
        assert section.day == 1

    def test_hour(self, section: PDS) -> None:
        assert section.hour == 0

    def test_minute(self, section: PDS) -> None:
        assert section.minute == 0

    def test_unitOfTimeRange(self, section: PDS) -> None:
        assert section.unitOfTimeRange == 1

    def test_P1(self, section: PDS) -> None:
        assert section.P1 == 0

    def test_P2(self, section: PDS) -> None:
        assert section.P2 == 6

    def test_timeRangeIndicator(self, section: PDS) -> None:
        assert section.timeRangeIndicator == 123

    def test_numberIncludedInAverage(self, section: PDS) -> None:
        assert section.numberIncludedInAverage == 124

    def test_numberMissingFromAveragesOrAccumulations(self, section: PDS) -> None:
        assert section.numberMissingFromAveragesOrAccumulations == 0

    def test_centuryOfReferenceTimeOfData(self, section: PDS) -> None:
        assert section.centuryOfReferenceTimeOfData == 20

    def test_subCentre(self, section: PDS) -> None:
        assert section.subCentre == 0

    def test_decimalScaleFactor(self, section: PDS) -> None:
        assert section.decimalScaleFactor == 0


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
        assert section.section2Length == 32

    def test_numberOfVerticalCoordinateValues(self, section: GDS) -> None:
        assert section.numberOfVerticalCoordinateValues == 0

    def test_pvlLocation(self, section: GDS) -> None:
        assert section.pvlLocation == 255

    def test_dataRepresentationType(self, section: GDS) -> None:
        assert section.dataRepresentationType == 0

    def test_Ni(self, section: GDS) -> None:
        assert section.Ni == 360 // 5

    def test_Nj(self, section: GDS) -> None:
        assert section.Nj == 90 // 3 + 1

    def test_latitudeOfFirstGridPoint(self, section: GDS) -> None:
        assert section.latitudeOfFirstGridPoint == 90000

    def test_longitudeOfFirstGridPoint(self, section: GDS) -> None:
        assert section.longitudeOfFirstGridPoint == -180000

    def test_resolutionAndComponentFlags(self, section: GDS) -> None:
        assert section.resolutionAndComponentFlags == 128

    def test_latitudeOfLastGridPoint(self, section: GDS) -> None:
        assert section.latitudeOfLastGridPoint == 0

    def test_longitudeOfLastGridPoint(self, section: GDS) -> None:
        assert section.longitudeOfLastGridPoint == 175000

    def test_iDirectionIncrement(self, section: GDS) -> None:
        assert section.iDirectionIncrement == 5000

    def test_jDirectionIncrement(self, section: GDS) -> None:
        assert section.jDirectionIncrement == 3000

    def test_scanningMode(self, section: GDS) -> None:
        assert section.scanningMode == 0


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
        assert section.section4Length == 6708

    def test_dataFlag(self, section: BDS) -> None:
        assert section.dataFlag == 8

    def test_binaryScaleFactor(self, section: BDS) -> None:
        assert section.binaryScaleFactor == -20

    def test_referenceValue(self, section: BDS) -> None:
        assert section.referenceValue == 0.0

    def test_bitsPerValue(self, section: BDS) -> None:
        assert section.bitsPerValue == 24

    def test_values(self, section: BDS) -> None:
        assert len(section.values) == 31 * 72
        assert section.values.dtype == np.uint32
        assert section.values.max() == 10 * (1 << 20)


class TestEndSection:
    section_name = "end"
    fieldnames = {"endOfMessage"}

    def test_fieldnames(self, section: EndSection) -> None:
        assert section.fieldnames == self.fieldnames

    def test_endOfMessage(self, section: EndSection) -> None:
        assert section.endOfMessage == b"7777"
