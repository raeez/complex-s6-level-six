TEX := pdflatex
FLAGS := -interaction=nonstopmode -halt-on-error -file-line-error
.PHONY: all check clean
all: out/paper.pdf
out/paper.pdf: paper.tex
	@mkdir -p build out
	@$(TEX) $(FLAGS) -output-directory=build paper.tex
	@$(TEX) $(FLAGS) -output-directory=build paper.tex
	@! grep -aEq 'Reference .* undefined|Citation .* undefined|There were undefined references' build/paper.log
	@cp build/paper.pdf out/paper.pdf
check: all
	@pdfinfo out/paper.pdf | grep '^Pages:'
clean:
	@rm -rf build out
