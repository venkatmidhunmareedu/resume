## Latex Resume

## Development Guide : 

1. Clone the repository : 
	- `git clone https://github.com/venkatmidhunmareedu/resume.git`
2. Install the necessary extensions and packages for your operating system. 
3. Build the project using 
	- Press `Ctrl + shift + p` to open the control panel and search for `LaTex Workshop: Build LaTex Project`
	- Or Simply Press `Ctrl + Shift + B` (which is a preset, see the settings yourself)
4. Go thorough the `resume.pdf` file. (The code build and saves the pdf on save that looks like live reload)


### Steps to preview the resume in VS Code or any other VS Code Fork.

1. Find `LaTex Workshop` extension and install it. ([https://marketplace.cursorapi.com/items/?itemName=James-Yu.latex-workshop](https://marketplace.visualstudio.com/items?itemName=James-Yu.latex-workshop))
2. If your platform is:
- Linux :
	- `sudo apt install texlive-latex-base texlive-fonts-recommended latexmk`
- Windows:
	- You have install `Perl` from [https://strawberryperl.com/](https://strawberryperl.com/)
	- if it's not installed already, open the `MikTeX` Package Manager and install the `latexmk` package.
- Mac:
	- It’s probably already installed.
	- If not, open `TeX Live Utility`, search for `latexmk` and install it.
	- If you prefer using the Terminal:
		- `sudo tlmgr install latexmk`

