#!/usr/bin/env python
"""validator: checks output file formats and basic requirements for the
submission to DGT task at WNGT 2019. Run the command as follows:

    $ python validate_outputs.py file_path

Tested with both Python 2 and 3.
"""
from __future__ import print_function

import json
import sys
import os.path as op

if sys.version_info[0] == 2:
    import codecs

    open = codecs.open
    STRING_TYPE = unicode
else:
    STRING_TYPE = str

TEST_IDS = set(
    [
        "03_01_17-Spurs-Pacers-ThehostSanAntonioSpurs",
        "11_01_16-Rockets-Cavaliers-TheClevelandCavaliersdefeatedthe",
        "02_24_17-Jazz-Bucks-TheUtahJazzdefeatedthe",
        "11_27_15-Grizzlies-Hawks-TheAtlantaHawks(11",
        "11_19_16-Suns-76ers-JoelEmbiidwassecondin",
        "12_26_16-Pelicans-Mavericks-TheNewOrleansPelicansdefeated",
        "02_08_16-Bulls-Hornets-TheCharlotteHornets(26",
        "01_21_15-Jazz-Cavaliers-TheClevelandCavaliers(23",
        "02_13_17-Warriors-Nuggets-TheDenverNuggetsdefeatedthe",
        "01_14_16-Raptors-Magic-TheTorontoRaptors(25",
        "01_03_17-Grizzlies-Lakers-TheLakerssnappedacold",
        "11_24_14-Knicks-Rockets-TheHoustonRockets(11",
        "02_09_15-Spurs-Pacers-TheSanAntonioSpurs(",
        "03_04_15-Suns-Magic-ThePhoenixSuns(32",
        "03_28_16-Kings-Trail Blazers-ThePortlandTrailBlazers(",
        "02_06_17-Timberwolves-Heat-GoranDragicwassensationalin",
        "02_21_15-Raptors-Rockets-TheTorontoRaptors(37",
        "12_26_16-Suns-Rockets-TheHoustonRocketsdefeatedthe",
        "03_13_17-Lakers-Nuggets-TheDenverNuggetspostedsome",
        "01_19_15-Pacers-Rockets-TheHoustonRockets(29",
        "12_19_16-Thunder-Hawks-Mondaynight'saffairwas",
        "11_19_14-Suns-Pistons-TheSuns(7-",
        "12_22_16-Heat-Lakers-Thesearetwoteamsthat",
        "01_19_16-Pelicans-Timberwolves-Afterallowingamassive38",
        "03_06_17-Pacers-Hornets-TheCharlotteHornetsdefeatedthe",
        "03_19_16-Nuggets-Hornets-TheDenverNuggets(29",
        "12_04_15-Lakers-Hawks-TheAtlantaHawks(13",
        "01_28_17-Clippers-Warriors-TheWarriorshaveabusedteams",
        "03_21_16-Magic-Celtics-TheBostonCeltics(41",
        "03_27_15-Jazz-Nuggets-TheDenverNuggets(28",
        "11_04_15-Wizards-Spurs-TheWashingtonWizards(3",
        "03_05_16-Spurs-Kings-TheSanAntonioSpurs(",
        "01_04_17-Magic-Hawks-Despitethelopsidedscoreline,",
        "11_28_16-Warriors-Hawks-ThehostGoldenStateWarriors",
        "01_28_15-Rockets-Mavericks-TheHoustonRockets(32",
        "11_14_16-76ers-Rockets-JoelEmbiidcontinuestobe",
        "03_18_15-76ers-Pistons-ThePhiladelphia76ers(16",
        "11_04_16-Knicks-Bulls-TheBullshungaroundall",
        "11_23_16-76ers-Grizzlies-TheMemphisGrizzliesdefeatedthe",
        "05_01_14-Thunder-Grizzlies-MEMPHIS-KevinDurantovercame",
        "12_12_14-Suns-Pistons-TheDetroitPistons(4",
        "01_04_17-Cavaliers-Bulls-Therecentformofthese",
        "01_29_16-Pistons-Cavaliers-TheClevelandCavaliers(33",
        "01_16_17-Knicks-Hawks-TheAtlantaHawksdefeatedthe",
        "02_03_17-Bucks-Nuggets-TheDenverNuggetsdefeatedthe",
        "02_10_17-Bucks-Lakers-TheLosAngelesLakersdefeated",
        "01_09_16-Jazz-Heat-TheUtahJazz(16",
        "05_03_16-Raptors-Heat-TheMiamiHeatdefeatedthe",
        "04_05_16-Suns-Hawks-TheAtlantaHawks(46",
        "02_15_17-Heat-Rockets-TheMiamiHeatdefeatedthe",
        "10_28_15-Knicks-Bucks-TheKnicksdominatedtheBucks",
        "12_27_14-Kings-Knicks-TheSacramentoKings(13",
        "01_03_17-Grizzlies-Lakers-TheLosAngelesLakershad",
        "03_11_15-Suns-Timberwolves-ThePhoenixSuns(34",
        "02_07_17-Magic-Rockets-TheHoustonRocketsdefeatedthe",
        "12_06_16-Pistons-Bulls-TheDetroitPistonsdefeatedthe",
        "11_22_16-Nuggets-Bulls-ThisresultnowmarksDenver",
        "12_13_16-Grizzlies-Cavaliers-KevinLove's29-",
        "12_15_15-Kings-Rockets-TheSacramentoKings(10",
        "03_30_16-Wizards-Kings-TheSacramentoKings(30",
        "01_24_15-76ers-Grizzlies-TheMemphisGrizzlies(31",
        "01_04_16-Heat-Pacers-Ittookovertimeforthe",
        "11_21_14-Thunder-Nets-TheBrooklynNets(5",
        "01_21_15-Pacers-Hawks-TheAtlantaHawks(35",
        "03_01_17-Wizards-Raptors-BojanBogdanovicandBradleyBeal",
        "11_01_14-Pistons-Nets-TheBrooklynNets(1",
        "02_13_17-Grizzlies-Nets-TheMemphisGrizzliesdefeatedthe",
        "12_15_15-Timberwolves-Nuggets-TheDenverNuggets(11",
        "11_08_16-Cavaliers-Hawks-TheAtlantaHawksdefeatedthe",
        "01_27_15-Warriors-Bulls-TheGoldenStateWarriors(",
        "11_11_16-76ers-Pacers-JoelEmbiidinsuredtheSixers",
        "02_04_16-Pelicans-Lakers-TheLosAngelesLakers(",
        "01_07_15-Suns-Timberwolves-ThePhoenixSuns(22",
        "02_24_17-Spurs-Clippers-TheSpurssawasolid",
        "01_24_17-Raptors-Spurs-WithTonyParkerbattlinga",
        "02_26_17-Suns-Bucks-It'sraretosee",
        "03_29_17-Pelicans-Mavericks-WhilepairingAnthonyDaviswith",
        "11_12_15-Jazz-Heat-TheMiamiHeat(6",
        "12_27_16-Thunder-Heat-Westbrookhasbeenmakingtriple",
        "11_15_16-Heat-Hawks-InjurieshaveledtoDion",
        "03_24_16-Cavaliers-Nets-TheBrooklynNets(20",
        "01_13_17-Celtics-Hawks-TheBostonCelticshungon",
        "02_11_15-Spurs-Pistons-TheSanAntonioSpurs(",
        "03_27_16-Pacers-Rockets-TheIndianaPacers(39",
        "11_20_16-Thunder-Pacers-Thepointguardsforboth",
        "03_24_17-Wizards-Nets-TheWashingtonbenchcombinedto",
        "04_03_15-Raptors-Nets-TheBrooklynNets(35",
        "10_29_16-Kings-Timberwolves-RudyGayandDeMarcusCousins",
        "03_11_17-76ers-Clippers-TheSixersenteredthefourth",
        "02_08_17-Jazz-Pelicans-ThevisitingUtahJazzdestroyed",
        "01_04_15-Knicks-Bucks-TheMilwaukeeBucks(18",
        "03_22_17-Jazz-Knicks-ThehostUtahJazzdefeated",
        "12_05_16-Trail Blazers-Bulls-ThePortlandTrailBlazersdefeated",
        "10_29_16-Magic-Cavaliers-TheClevelandCavaliersdefeatedthe",
        "02_02_15-Wizards-Hornets-TheCharlotteHornets(21",
        "01_03_17-76ers-Timberwolves-ThePhiladelphia76ersdefeatedthe",
        "03_08_15-Lakers-Mavericks-TheDallasMavericks(41",
        "01_15_16-Suns-Celtics-TheBostonCeltics(21",
        "11_13_16-Timberwolves-Lakers-Theseweretwoteamsheaded",
        "02_24_16-Raptors-Timberwolves-TheTorontoRaptors(38",
        "12_30_15-Magic-Nets-TheOrlandoMagic(19",
        "04_08_15-Suns-Mavericks-TheDallasMavericks(47",
        "02_25_17-Heat-Pacers-TheMiamiHeatdefeatedthe",
        "11_21_16-Timberwolves-Celtics-ThevisitingBostonCelticsdefeated",
        "01_04_17-Grizzlies-Clippers-WithChrisPaulandBlake",
        "11_30_15-Thunder-Hawks-TheAtlantaHawks(12",
        "12_05_16-Jazz-Lakers-LouWilliamsledallscorers",
        "11_15_14-Spurs-Kings-TheSacramentoKings(6",
        "12_30_15-Trail Blazers-Nuggets-ThePortlandTrailBlazers(",
        "11_25_14-Bucks-Pistons-TheMilwaukeeBucks(8",
        "02_11_17-Suns-Rockets-TheHoustonRocketsdefeatedthe",
        "03_19_16-Jazz-Bulls-TheChicagoBulls(35",
        "01_20_15-Spurs-Nuggets-TheSanAntonioSpurs(",
        "03_29_15-Wizards-Rockets-TheHoustonRockets(50",
        "04_26_15-Cavaliers-Celtics-Thesecond-seedCleveland",
        "12_01_16-Rockets-Warriors-TheHoustonRocketsdefeatedthe",
        "02_28_15-Mavericks-Nets-TheBrooklynNets(24",
        "01_04_16-Trail Blazers-Grizzlies-TheMemphisGrizzlies(19",
        "01_31_17-Spurs-Thunder-KawhiLeonardhasputtogether",
        "03_08_17-Wizards-Nuggets-TheWashingtonWizardsdefeatedthe",
        "03_25_17-Trail Blazers-Timberwolves-TheBlazerscollectivelyshotan",
        "12_06_15-Suns-Grizzlies-TheMemphisGrizzlies(12",
        "11_16_14-Knicks-Nuggets-TheNewYorkKnicks(",
        "10_30_15-Raptors-Celtics-TheTorontoRaptors(20",
        "04_11_15-Raptors-Heat-TheMiamiHeat(35",
        "11_20_14-Heat-Clippers-TheLosAngelesClippers(",
        "12_07_15-Pelicans-Celtics-TheBostonCelticstookcare",
        "05_03_16-Trail Blazers-Warriors-TheGoldenStateWarriorsdefeated",
        "11_29_15-Lakers-Pacers-TheIndianaPacers(11",
        "04_11_16-Jazz-Mavericks-TheDallasMavericks(42",
        "12_18_15-Raptors-Heat-TheTorontoRaptors(17",
        "12_28_15-Spurs-Timberwolves-TheSanAntonioSpurs(",
        "12_25_14-Spurs-Thunder-TheOklahomaCityThunder(",
        "03_22_16-Pelicans-Heat-TheMiamiHeat(41",
        "11_26_16-Wizards-Spurs-ThevisitingSanAntonioSpurs",
        "12_28_14-Trail Blazers-Knicks-ThePortlandTrailBlazers(",
        "05_22_16-Thunder-Warriors-TheOklahomaCityThunderblew",
        "11_16_16-Mavericks-Celtics-TheBostonCelticsdefeatedthe",
        "12_09_15-Grizzlies-Pistons-TheMemphisGrizzlies(13",
        "12_01_14-Wizards-Heat-TheWashingtonWizards(11",
        "12_25_15-Warriors-Cavaliers-TheGoldenStateWarriors(",
        "12_15_15-Bucks-Lakers-TheLosAngelesLakers(",
        "04_01_16-Raptors-Grizzlies-TheTorontoRaptors(51",
        "12_23_15-Hornets-Celtics-TheBostonCeltics(16",
        "11_04_14-Heat-Rockets-TheHoustonRockets(50",
        "04_19_15-Cavaliers-Celtics-TheClevelandCavaliers(53",
        "11_23_16-Kings-Thunder-ThehostSacramentoKingsdefeated",
        "12_10_16-Rockets-Mavericks-Houstonwasexpectedtowin",
        "12_03_14-Bucks-Mavericks-TheDallasMavericks(15",
        "11_12_16-Timberwolves-Clippers-TheClippershavebeendominating",
        "11_21_14-Suns-76ers-ThePhoenixSuns(8",
        "11_07_15-Spurs-Hornets-TheSanAntonioSpurs(",
        "03_15_17-Spurs-Trail Blazers-ThePortlandTrailBlazersdefeated",
        "10_26_16-Raptors-Pistons-TheRaptorsdidn'tneed",
        "11_13_16-Trail Blazers-Nuggets-Itwasatoughnight",
        "01_17_15-Trail Blazers-Grizzlies-TheMemphisGrizzlies(29",
        "11_29_15-Knicks-Rockets-TheHoustonRockets(7",
        "11_10_15-Timberwolves-Hornets-TheCharlotteHornets(3",
        "02_08_15-Magic-Bulls-TheChicagoBulls(32",
        "01_29_16-Mavericks-Nets-TheDallasMavericks(27",
        "02_04_17-76ers-Heat-TheMiamiHeatdefeatedthe",
        "02_13_17-Spurs-Pacers-TheSanAntonioSpursdefeated",
        "12_27_16-Rockets-Mavericks-Itwasanotherdayat",
        "12_01_16-Clippers-Cavaliers-TheLosAngelesClippersdefeated",
        "02_27_17-Kings-Timberwolves-TheMinnesotaTimberwolvesdefeatedthe",
        "01_18_16-Pistons-Bulls-TheChicagoBulls(24",
        "12_28_16-Wizards-Pacers-TheWashingtonWizardsdefeatedthe",
        "12_27_14-Pacers-Nets-TheIndianaPacers(11",
        "03_27_17-Thunder-Mavericks-Inhasn'tbeenthe",
        "02_05_15-Trail Blazers-Suns-ThePortlandTrailBlazers(",
        "11_17_14-Clippers-Bulls-TheChicagoBulls(8",
        "12_29_16-Lakers-Mavericks-TheDallasMavericksdefeatedthe",
        "12_12_16-Pacers-Hornets-TheIndianaPacersdefeatedthe",
        "11_21_15-76ers-Heat-TheMiamiHeat(8",
        "12_03_16-Timberwolves-Hornets-AndrewWigginsandKarl-AnthonyTowns",
        "01_05_16-Kings-Mavericks-TheDallasMavericks(20",
        "03_19_17-Trail Blazers-Heat-ThePortlandTrailBlazerssaw",
        "03_20_16-Trail Blazers-Mavericks-TheDallasMavericks(35",
        "12_30_15-Wizards-Raptors-TheTorontoRaptors(20",
        "03_20_17-Rockets-Nuggets-TheHoustonRocketsdefeatedthe",
        "12_12_14-Trail Blazers-Bulls-TheBulls(14-",
        "02_12_17-Spurs-Knicks-It'susuallytheSpurs",
        "03_11_17-76ers-Clippers-TheLosAngelesClippersdefeated",
        "11_28_14-Raptors-Mavericks-TheDallasMavericks(12",
        "03_04_17-Clippers-Bulls-TheLosAngelesClippersdefeated",
        "12_02_16-Pistons-Hawks-TheDetroitPistonsdefeatedthe",
        "12_29_14-Kings-Nets-DespitebigperformancesfromDeMarcus",
        "01_29_17-Spurs-Mavericks-ThevisitingDallasMaverickstook",
        "03_17_16-Heat-Hornets-TheCharlotteHornets(39",
        "12_21_16-Suns-Rockets-Itwasabignight",
        "03_29_17-Pelicans-Mavericks-TheNewOrleansPelicansdefeated",
        "01_15_16-Thunder-Timberwolves-TheOklahomaCityThunder(",
        "01_07_16-Bulls-Celtics-TheChicagoBulls(22",
        "11_30_16-Wizards-Thunder-TheOklahomaCityThunderdefeated",
        "04_10_15-Nuggets-Mavericks-TheDallasMavericks(48",
        "03_18_15-Warriors-Hawks-TheGoldenStateWarriors(",
        "12_29_16-Raptors-Suns-ThehostPhoenixSunstook",
        "01_27_16-Spurs-Rockets-TheSanAntonioSpurs(",
        "10_30_16-Jazz-Clippers-TheLosAngelesClippersdefeated",
        "01_07_17-Pelicans-Celtics-MarcusSmartproduced22points",
        "02_03_16-Spurs-Pelicans-TheSanAntonioSpurs(",
        "10_27_15-Cavaliers-Bulls-WithPresidentBarackObamain",
        "10_28_14-Spurs-Mavericks-TheSanAntonioSpurs(",
        "02_24_17-Heat-Hawks-ThevisitingMiamiHeathandily",
        "11_04_16-Lakers-Warriors-WhiletheWarriorshaveseen",
        "03_22_17-Pistons-Bulls-TheChicagoBullsdefeatedthe",
        "11_06_16-Raptors-Kings-DespitetheSacramentoKingslosing",
        "12_05_15-Trail Blazers-Timberwolves-ThePortlandTrailBlazers(",
        "01_17_15-Timberwolves-Nuggets-TheMinnesotaTimberwolves(7",
        "01_21_17-Bucks-Heat-Thesearetwoteamsgoing",
        "01_23_17-Wizards-Hornets-TheWashingtonWizardsdefeatedthe",
        "11_02_16-Bulls-Celtics-TheBostonCelticsdefeatedthe",
        "01_03_15-Trail Blazers-Hawks-TheAtlantaHawks(25",
        "12_02_14-Lakers-Pistons-TheLosAngelesLakers(",
        "12_27_15-Thunder-Nuggets-TheOklahomaCityThunder(",
        "12_07_16-Lakers-Rockets-Wednesdaynight'sshowdownin",
        "11_01_15-Spurs-Celtics-Intheirfirstoftwo",
        "02_08_17-Spurs-76ers-TheSanAntonioSpursdefeated",
        "12_11_16-76ers-Pistons-JahlilOkaforandT.J.McConnell",
        "03_17_15-Pelicans-Bucks-TheNewOrleansPelicans(",
        "01_06_16-Knicks-Heat-TheNewYorkKnicks(",
        "11_08_16-Timberwolves-Nets-TheBrooklynNetsdefeatedthe",
        "12_10_16-Pelicans-Clippers-ChrisPaulrackedupone",
        "11_25_16-Lakers-Warriors-TheGoldenStateWarriorsdefeated",
        "01_28_17-Timberwolves-Nets-Karl-AnthonyTownswentofffor",
        "01_08_17-Raptors-Rockets-TheHoustonRocketsdefeatedthe",
        "12_23_15-76ers-Bucks-TheMilwaukeeBucks(12",
        "01_07_17-Spurs-Hornets-TheSanAntonioSpursdefeated",
        "11_27_15-Pacers-Bulls-TheIndianaPacers(10",
        "01_14_17-Lakers-Clippers-ThehostLosAngelesClippers",
        "11_05_16-Pistons-Nuggets-TheDetroitPistonsdefeatedthe",
        "01_05_16-Bucks-Bulls-TheChicagoBulls(21",
        "11_28_16-Wizards-Kings-DeMarcusCousinsexplodedfora",
        "03_10_16-Spurs-Bulls-TheSanAntonioSpurs(",
        "03_07_16-Magic-Warriors-TheGoldenStateWarriors(",
        "12_07_15-Trail Blazers-Bucks-TheMilwaukeeBucks(9",
        "01_13_15-Heat-Lakers-TheMiamiHeat(17",
        "12_17_16-Knicks-Nuggets-TheDenverNuggetsdefeatedthe",
        "12_22_14-Mavericks-Hawks-TheAtlantaHawks(20",
        "04_12_15-Lakers-Mavericks-TheDallasMavericks(49",
        "03_27_15-Knicks-Celtics-TheBostonCeltics(32",
    ]
)


def assert_quit(condition, msg):
    try:
        assert condition
    except AssertionError:
        print(msg)
        sys.exit(1)


def validate_record(record, idx):
    id_, summary = record["id"], record["summary"]

    assert_quit(
        id_ in TEST_IDS,"{}-th record has the unrecognized ID: {}".format(idx, id_)
    )
    assert_quit(
        isinstance(summary, list), "{}-th record's summary isn't a list.".format(idx)
    )

    summary_types = set(type(s) for s in summary)
    assert_quit(
        len(summary_types) == 1 and list(summary_types)[0] == STRING_TYPE,
        "{}-th record's summary has to be a list of strings.".format(idx),
    )


def validate(obj):

    assert_quit(isinstance(obj, list), "Loaded data has to be a list of dictionaries.")

    for idx, record in enumerate(obj):
        assert_quit(isinstance(record, dict), "{}-th record is not valid.".format(idx))

        assert_quit("id" in record, "{}-th record doesn't have 'id' field.".format(idx))
        assert_quit(
            "summary" in record,
            "{}-th record doesn't have 'summary' field.".format(idx),
        )

        validate_record(record, idx)

    ids = [r["id"] for r in obj]
    assert_quit(len(ids) == len(set(ids)), "Some IDs are duplicated.")

    missed = TEST_IDS - set(ids)
    assert_quit(
        len(missed) == 0, "The following IDs are missed: {}".format(list(missed))
    )

    print("All good! Please go ahead and submit.")


if __name__ == "__main__":

    # Check if a file even exists.
    usage = (
        "Usage: python validate_outputs.py file_path\n"
        "\tfile_path - Path to your submission file in a JSON format."
    )
    assert_quit(len(sys.argv) == 2 and op.isfile(sys.argv[1]), usage)

    # Check if the file is a valid JSON.
    with open(sys.argv[1], "r", encoding="utf8") as f:
        try:
            content = json.load(f)

        except ValueError:
            msg = "File could not be loaded. " "Please make sure you have a JSON file."
            assert_quit(False, msg)

    validate(content)
