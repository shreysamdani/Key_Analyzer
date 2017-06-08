# Key_Analyzer
This tool is used to analyze seed/key data in the form of an excel document.</br></br>

## Features:</br>
Given hex seed/key pairs, this tool conducts basic analysis on the data, including</br>
<ul>
<li>DEC BIN conversion
<li>XOR, first differences, and second differences
<li>Binary differences
<li>Graphs and Charts
<li>Binary Rotations and Shifts
<li>Common Appearances</ul></br>

## Formatting: </br>
The input excel file should have a sheet named Seed_Keys_Samples. The first column of this sheet should be the hex seeds and the second column should be the hex keys. Row 2 of this sheet must have 'SEED' and 'KEY' in columns A and B respectively. The values must follow immediately after. If the file is not reading in, change the format of the cells to 'text' rather than general.

## Usage:</br>

### Simple (Executable):</br>
Download or clone the git repository. To run this program, open the platform specific folder and run the file named Analyzer or Analyzer.exe. Drag and drop the excel file into the terminal and click enter.</br>
The excel file will then open.

### Advanced (Running python):</br>

#### Prerequisites: </br>
<ul>
<li>python3
<li>pandas 
<li>xlsxwriter 
<li>numpy
<li>PyQt5
</ul>

##### OSX:
Open terminal and run the following to install:</br>
<pre><code>sudo pip install pandas
</code></pre>
<pre><code>sudo pip install xlrd
</code></pre></ul>
<pre><code>sudo pip install numpy
</code></pre></ul>
<pre><code>sudo pip install PyQt5
</code></pre></ul></br>

##### Windows:
Run cmd as administrator and execute the following:</br>
<pre><code>pip install pandas
</code></pre>
<pre><code>pip install xlrd
</code></pre></ul>
<pre><code>pip install numpy
</code></pre></ul>
<pre><code>pip install PyQt5
</code></pre></ul></br>

#### Running the code:</br>
Navigate to the python directory. Run 
<pre><code>python3 Analyzer.py
</code></pre></ul></br>
Then drag and drop the file into terminal and click enter.
