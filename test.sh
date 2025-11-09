
run_edgar_test() {
  python3 -m src.searchers.test_scripts test_edgar
}

run_macrotrends_stocks() {
  python3 -m src.searchers.test_scripts test_macrotrends_stocks
}

run_macrotreds_history() {
  python3 -m src.searchers.test_scripts test_macrotrends_history "$1"
}

run_nasdaq_test() {
  python3 -m src.searchers.test_scripts test_nasdaq_news "$1" "$2"
}

if [ "$1" = "edgar" ]; then
  run_edgar_test
elif [ "$1" = "macro_h" ]; then
  run_macrotreds_history "$2"
elif [ "$1" = "macro_s" ]; then
  run_macrotrends_stocks
elif [ "$1" = "nasdaq" ]; then
  run_nasdaq_test "$2" "$3"
fi
