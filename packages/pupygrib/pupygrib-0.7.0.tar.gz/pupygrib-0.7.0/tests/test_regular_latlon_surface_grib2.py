"""Regression tests for reading regular_latlon_surface.grib2."""

import datetime

import pytest

from pupygrib import Message
from pupygrib.edition2 import (
    BitMapSection,
    DataRepresentationSection,
    DataSection,
    EndSection,
    GridDescriptionSection,
    IdentificationSection,
    IndicatorSection,
    LocalUseSection,
    ProductDefinitionSection,
)

gribfile = "data/regular_latlon_surface.grib2"


class TestIndicatorSection:
    section_name = "is_"
    fieldnames = {"identifier", "discipline", "editionNumber", "totalLength"}

    def test_fieldnames(self, section: IndicatorSection) -> None:
        assert section.fieldnames == self.fieldnames

    def test_identifier(self, section: IndicatorSection) -> None:
        assert section.identifier == b"GRIB"

    def test_discipline(self, section: IndicatorSection) -> None:
        assert section.discipline == 0

    def test_editionNumber(self, section: IndicatorSection) -> None:
        assert section.editionNumber == 2

    def test_totalLength(self, section: IndicatorSection) -> None:
        assert section.totalLength == 1188


class TestIdentificationSection:
    section_name = "ids"
    fieldnames = {
        "section1Length",
        "numberOfSection",
        "centre",
        "subCentre",
        "tablesVersion",
        "localTablesVersion",
        "significanceOfReferenceTime",
        "year",
        "month",
        "day",
        "hour",
        "minute",
        "second",
        "productionStatusOfProcessedData",
        "typeOfProcessedData",
    }

    def test_fieldnames(self, section: IdentificationSection) -> None:
        assert section.fieldnames == self.fieldnames

    def test_section1Length(self, section: IdentificationSection) -> None:
        assert section.section1Length == 21

    def test_numberOfSection(self, section: IdentificationSection) -> None:
        assert section.numberOfSection == 1

    def test_centre(self, section: IdentificationSection) -> None:
        assert section.centre == 98

    def test_subCentre(self, section: IdentificationSection) -> None:
        assert section.subCentre == 0

    def test_tablesVersion(self, section: IdentificationSection) -> None:
        assert section.tablesVersion == 5

    def test_localTablesVersion(self, section: IdentificationSection) -> None:
        assert section.localTablesVersion == 0

    def test_significanceOfReferenceTime(self, section: IdentificationSection) -> None:
        assert section.significanceOfReferenceTime == 1

    def test_year(self, section: IdentificationSection) -> None:
        assert section.year == 2008

    def test_month(self, section: IdentificationSection) -> None:
        assert section.month == 2

    def test_day(self, section: IdentificationSection) -> None:
        assert section.day == 6

    def test_hour(self, section: IdentificationSection) -> None:
        assert section.hour == 12

    def test_minute(self, section: IdentificationSection) -> None:
        assert section.minute == 0

    def test_second(self, section: IdentificationSection) -> None:
        assert section.second == 0

    def test_productionStatusOfProcessedData(
        self, section: IdentificationSection
    ) -> None:
        assert section.productionStatusOfProcessedData == 0

    def test_typeOfProcessedData(self, section: IdentificationSection) -> None:
        assert section.typeOfProcessedData == 255


class TestLocalUseSection:
    section_name = "loc"
    fieldnames = {"section2Length", "numberOfSection"}

    def test_fieldnames(self, section: LocalUseSection) -> None:
        assert section.fieldnames == self.fieldnames

    def test_section2Length(self, section: LocalUseSection) -> None:
        assert section.section2Length == 17

    def test_numberOfSection(self, section: LocalUseSection) -> None:
        assert section.numberOfSection == 2


class TestGridDescriptionSection:
    section_name = "gds"
    fieldnames = {
        "section3Length",
        "numberOfSection",
        "sourceOfGridDefinition",
        "numberOfDataPoints",
        "numberOfOctetsForNumberOfPoints",
        "interpretationOfNumberOfPoints",
        "gridDefinitionTemplateNumber",
    }

    def test_fieldnames(self, section: GridDescriptionSection) -> None:
        assert section.fieldnames == self.fieldnames

    def test_section3Length(self, section: GridDescriptionSection) -> None:
        assert section.section3Length == 72

    def test_numberOfSection(self, section: GridDescriptionSection) -> None:
        assert section.numberOfSection == 3

    def test_sourceOfGridDefinition(self, section: GridDescriptionSection) -> None:
        assert section.sourceOfGridDefinition == 0

    def test_numberOfDataPoints(self, section: GridDescriptionSection) -> None:
        assert section.numberOfDataPoints == 496

    def test_numberOfOctetsForNumberOfPoints(
        self, section: GridDescriptionSection
    ) -> None:
        assert section.numberOfOctetsForNumberOfPoints == 0

    def test_interpretationOfNumberOfPoints(
        self, section: GridDescriptionSection
    ) -> None:
        assert section.interpretationOfNumberOfPoints == 0

    def test_gridDefinitionTemplateNumber(
        self, section: GridDescriptionSection
    ) -> None:
        assert section.gridDefinitionTemplateNumber == 0


class TestProductDefinitionSection:
    section_name = "pds"
    fieldnames = {
        "section4Length",
        "numberOfSection",
        "NV",
        "productDefinitionTemplateNumber",
    }

    def test_fieldnames(self, section: ProductDefinitionSection) -> None:
        assert section.fieldnames == self.fieldnames

    def test_section4Length(self, section: ProductDefinitionSection) -> None:
        assert section.section4Length == 34

    def test_numberOfSection(self, section: ProductDefinitionSection) -> None:
        assert section.numberOfSection == 4

    def test_NV(self, section: ProductDefinitionSection) -> None:
        assert section.NV == 0

    def test_productDefinitionTemplateNumber(
        self, section: ProductDefinitionSection
    ) -> None:
        assert section.productDefinitionTemplateNumber == 0


class TestDataRepresentationSection:
    section_name = "drs"
    fieldnames = {
        "section5Length",
        "numberOfSection",
        "numberOfValues",
        "dataRepresentationTemplateNumber",
    }

    def test_fieldnames(self, section: DataRepresentationSection) -> None:
        assert section.fieldnames == self.fieldnames

    def test_section5Length(self, section: DataRepresentationSection) -> None:
        assert section.section5Length == 21

    def test_numberOfSection(self, section: DataRepresentationSection) -> None:
        assert section.numberOfSection == 5

    def test_numberOfValues(self, section: DataRepresentationSection) -> None:
        assert section.numberOfValues == 496

    def test_dataRepresentationTemplateNumber(
        self, section: DataRepresentationSection
    ) -> None:
        assert section.dataRepresentationTemplateNumber == 0


class TestBitMapSection:
    section_name = "bitmap"
    fieldnames = {"section6Length", "numberOfSection", "bitMapIndicator"}

    def test_fieldnames(self, section: BitMapSection) -> None:
        assert section.fieldnames == self.fieldnames

    def test_section6Length(self, section: BitMapSection) -> None:
        assert section.section6Length == 6

    def test_numberOfSection(self, section: BitMapSection) -> None:
        assert section.numberOfSection == 6

    def test_bitMapIndicator(self, section: BitMapSection) -> None:
        assert section.bitMapIndicator == 255


class TestDataSection:
    section_name = "data"
    fieldnames = {"section7Length", "numberOfSection"}

    def test_fieldnames(self, section: DataSection) -> None:
        assert section.fieldnames == self.fieldnames

    def test_section7Length(self, section: DataSection) -> None:
        assert section.section7Length == 997

    def test_numberOfSection(self, section: DataSection) -> None:
        assert section.numberOfSection == 7


class TestEndSection:
    section_name = "end"
    fieldnames = {"endOfMessage"}

    def test_fieldnames(self, section: EndSection) -> None:
        assert section.fieldnames == self.fieldnames

    def test_endOfMessage(self, section: EndSection) -> None:
        assert section.endOfMessage == b"7777"


class TestMessage:
    def test_time(self, message: Message) -> None:
        assert message.get_time() == datetime.datetime(2008, 2, 6, 12, 0)

    def test_coordinates(self, message: Message) -> None:
        with pytest.raises(NotImplementedError):
            message.get_coordinates()

    def test_values(self, message: Message) -> None:
        with pytest.raises(NotImplementedError):
            message.get_values()
