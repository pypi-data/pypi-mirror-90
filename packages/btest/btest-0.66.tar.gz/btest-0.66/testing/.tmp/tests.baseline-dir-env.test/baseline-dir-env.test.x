# %TEST-EXEC-FAIL: BTEST_BASELINE_DIR=mydir btest %INPUT
# %TEST-EXEC: test ! -e mydir/baseline-dir-env/output
# %TEST-EXEC: BTEST_BASELINE_DIR=mydir btest -U %INPUT
# %TEST-EXEC: test ! -e Baseline
# %TEST-EXEC: test -f mydir/baseline-dir-env/output
# %TEST-EXEC: BTEST_BASELINE_DIR=mydir btest %INPUT

@TEST-EXEC: echo Hello, World! >output
@TEST-EXEC: btest-diff output

