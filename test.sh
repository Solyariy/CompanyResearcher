
run_edgar_test() {
  python3 -m src.searchers.test_scripts test_edgar
}


if [ "$1" = "edgar" ]; then
  run_edgar_test
fi
