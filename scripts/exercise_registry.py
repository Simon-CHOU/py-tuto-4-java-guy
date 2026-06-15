"""Central exercise registry for root-level learning commands."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ExerciseSpec:
    question_id: str
    module_id: str
    module_dir: str
    symbol_name: str
    pytest_class_name: str


EXERCISES: tuple[ExerciseSpec, ...] = (
    ExerciseSpec("M01-Q01", "M01", "modules/01-basics-and-types", "classify_number", "TestClassifyNumber"),
    ExerciseSpec("M01-Q02", "M01", "modules/01-basics-and-types", "safe_divide", "TestSafeDivide"),
    ExerciseSpec("M01-Q03", "M01", "modules/01-basics-and-types", "format_table", "TestFormatTable"),
    ExerciseSpec("M01-Q04", "M01", "modules/01-basics-and-types", "is_palindrome", "TestIsPalindrome"),
    ExerciseSpec("M01-Q05", "M01", "modules/01-basics-and-types", "flatten_nested", "TestFlattenNested"),
    ExerciseSpec("M01-Q06", "M01", "modules/01-basics-and-types", "merge_defaults", "TestMergeDefaults"),
    ExerciseSpec("M01-Q07", "M01", "modules/01-basics-and-types", "parse_command", "TestParseCommand"),
    ExerciseSpec("M01-Q08", "M01", "modules/01-basics-and-types", "describe_shape", "TestDescribeShape"),
    ExerciseSpec(
        "M02-Q01",
        "M02",
        "modules/02-functional-features",
        "select_and_transform",
        "TestSelectAndTransform",
    ),
    ExerciseSpec(
        "M02-Q02",
        "M02",
        "modules/02-functional-features",
        "word_frequencies",
        "TestWordFrequencies",
    ),
    ExerciseSpec("M02-Q03", "M02", "modules/02-functional-features", "fibonacci", "TestFibonacci"),
    ExerciseSpec("M02-Q04", "M02", "modules/02-functional-features", "group_by", "TestGroupBy"),
    ExerciseSpec(
        "M02-Q05",
        "M02",
        "modules/02-functional-features",
        "running_average",
        "TestRunningAverage",
    ),
    ExerciseSpec("M02-Q06", "M02", "modules/02-functional-features", "interleave", "TestInterleave"),
    ExerciseSpec(
        "M02-Q07",
        "M02",
        "modules/02-functional-features",
        "create_counter",
        "TestCreateCounter",
    ),
    ExerciseSpec("M03-Q01", "M03", "modules/03-oop", "Vector2D", "TestVector2D"),
    ExerciseSpec("M03-Q02", "M03", "modules/03-oop", "BetterDict", "TestBetterDict"),
    ExerciseSpec("M03-Q03", "M03", "modules/03-oop", "Temperature", "TestTemperature"),
    ExerciseSpec("M03-Q04", "M03", "modules/03-oop", "ImmutableConfig", "TestImmutableConfig"),
    ExerciseSpec("M03-Q05", "M03", "modules/03-oop", "ConfigRecord", "TestConfigRecord"),
    ExerciseSpec(
        "M04-Q01",
        "M04",
        "modules/04-interfaces-and-abstraction",
        "DictStore",
        "TestDictStore",
    ),
    ExerciseSpec(
        "M04-Q02",
        "M04",
        "modules/04-interfaces-and-abstraction",
        "LRUStore",
        "TestLRUStore",
    ),
    ExerciseSpec(
        "M04-Q03",
        "M04",
        "modules/04-interfaces-and-abstraction",
        "save_to_file",
        "TestSaveToFile",
    ),
    ExerciseSpec(
        "M05-Q01",
        "M05",
        "modules/05-modules-and-packages",
        "import_from_path",
        "TestImportFromPath",
    ),
    ExerciseSpec(
        "M05-Q02",
        "M05",
        "modules/05-modules-and-packages",
        "validate_package_structure",
        "TestValidatePackageStructure",
    ),
    ExerciseSpec(
        "M05-Q03",
        "M05",
        "modules/05-modules-and-packages",
        "detect_circular_imports",
        "TestDetectCircularImports",
    ),
    ExerciseSpec(
        "M05-Q04",
        "M05",
        "modules/05-modules-and-packages",
        "create_init_reexport",
        "TestCreateInitReexport",
    ),
    ExerciseSpec(
        "M05-Q05",
        "M05",
        "modules/05-modules-and-packages",
        "filter_imports",
        "TestFilterImports",
    ),
    ExerciseSpec(
        "M06-Q01",
        "M06",
        "modules/06-decorators-and-context-managers",
        "timer",
        "TestTimer",
    ),
    ExerciseSpec(
        "M06-Q02",
        "M06",
        "modules/06-decorators-and-context-managers",
        "retry",
        "TestRetry",
    ),
    ExerciseSpec(
        "M06-Q03",
        "M06",
        "modules/06-decorators-and-context-managers",
        "memoize",
        "TestMemoize",
    ),
    ExerciseSpec(
        "M06-Q04",
        "M06",
        "modules/06-decorators-and-context-managers",
        "TimedOpen",
        "TestTimedOpen",
    ),
    ExerciseSpec(
        "M06-Q05",
        "M06",
        "modules/06-decorators-and-context-managers",
        "validate_types",
        "TestValidateTypes",
    ),
    ExerciseSpec("M07-Q01", "M07", "modules/07-type-hints", "Stack", "TestStack"),
    ExerciseSpec("M07-Q02", "M07", "modules/07-type-hints", "first", "TestFirst"),
    ExerciseSpec(
        "M07-Q03",
        "M07",
        "modules/07-type-hints",
        "typed_deserialize",
        "TestTypedDeserialize",
    ),
    ExerciseSpec(
        "M08-Q01",
        "M08",
        "modules/08-concurrency-and-parallelism",
        "sequential_sum",
        "TestSequentialSum",
    ),
    ExerciseSpec(
        "M08-Q02",
        "M08",
        "modules/08-concurrency-and-parallelism",
        "threaded_sum",
        "TestThreadedSum",
    ),
    ExerciseSpec(
        "M08-Q03",
        "M08",
        "modules/08-concurrency-and-parallelism",
        "process_sum",
        "TestProcessSum",
    ),
    ExerciseSpec(
        "M08-Q04",
        "M08",
        "modules/08-concurrency-and-parallelism",
        "gil_demonstration",
        "TestGILDemonstration",
    ),
    ExerciseSpec(
        "M08-Q05",
        "M08",
        "modules/08-concurrency-and-parallelism",
        "countdown",
        "TestCountdown",
    ),
    ExerciseSpec("M09-Q01", "M09", "modules/09-asyncio", "async_fetch_all", "TestAsyncFetchAll"),
    ExerciseSpec("M09-Q02", "M09", "modules/09-asyncio", "async_countdown", "TestAsyncCountdown"),
    ExerciseSpec(
        "M09-Q03",
        "M09",
        "modules/09-asyncio",
        "run_concurrently",
        "TestRunConcurrently",
    ),
    ExerciseSpec("M09-Q04", "M09", "modules/09-asyncio", "async_timer", "TestAsyncTimer"),
)

_BY_QUESTION_ID = {exercise.question_id: exercise for exercise in EXERCISES}


def list_exercises() -> tuple[ExerciseSpec, ...]:
    return EXERCISES


def get_exercise(question_id: str) -> ExerciseSpec:
    return _BY_QUESTION_ID[question_id]
