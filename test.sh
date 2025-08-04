
run_edgar_test() {
  python3 -m src.searchers.test_scripts test_edgar
}

test_macrotrends_stocks() {
  python3 -m src.searchers.test_scripts test_macrotrends_stocks
}

run_macrotreds_history() {
  python3 -m src.searchers.test_scripts test_macrotrends_history "$1"
}

if [ "$1" = "edgar" ]; then
  run_edgar_test
elif [ "$1" = "macro_h" ]; then
  run_macrotreds_history "$2"
elif [ "$1" = "macro_s" ]; then
  test_macrotrends_stocks
fi
