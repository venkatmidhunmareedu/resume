.PHONY: cleanup-ignored

cleanup-ignored:
	git clean -ndX
	git clean -fdX
