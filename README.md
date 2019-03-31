
Things to follow to run this application :

1] Install Python(3.6) and PyQt5 and other dependencies

       i] pip install pyqt5
       
      ii] pip install numpy
      
     iii] pip install matplotlib
     
      iv] pip install pil
      
       v] pip install tkinter
       
       OR run the commmand : 'pip install -r requirements.txt' (add the file in the project folder)
         

Name of Application : CSV viewer

Features:

Data Display Tab : Base template for displaying data in tabular view

1] File Menu:

      a] Load : Loads a csv file into a tabular view
      
      b] Save : Helps to save .csv files
      
      c] Save Plots : Saves plots without displaying plots as a png file , with a dialog box for selected coloumns
      
      i]   Save_1 : For saving a scatterplot
      ii]  Save_2 : For saving a scatterplot with smoothlines
      iii] Save_3 : For saving a plot with lines
   
      d] Add Data
      
         i] Add Row : Add extra row at the end
         
         ii] Add Column : Add extra col at the end
         
      e] Clear : Clear data from the window 

2] Edit Menu:

      a] Edit Data : Helps to make loaded data editable
      
      
      b] Remove Data 
      
         i] Delete Row : remove the selected row
         
         ii] Delete Column : remove the selected col 

3] Scatterplot tab:

	a] Plot Data : (Plotting Data with appropriate X & Y-axis label and a title)
  
	b] Save as png : opens a dialog box for location to save the plot
  
4] Scatterplot with smooth lines tab:

	a] Plot Data : (Plotting Data with appropriate X & Y-axis label and a title)
  
	b] Save as png : opens a dialog box for location to save the plot
  
5] Scatterplot with lines tab:

	a] Plot Data : (Plotting Data with appropriate X & Y-axis label and a title)
  
	b] Save as png : opens a dialog box for location to save the plot
 

*PLOTING EXCEPTIONS* : Integrated every handling for errors that can be commited during plotting 

	a]If user selects more than two coloumns 
  
	b]If user selects invalid coloumn i.e maybe character data for plotting
  
