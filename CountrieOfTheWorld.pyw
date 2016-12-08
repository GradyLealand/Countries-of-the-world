import sys, csv

from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox
from PyQt5.QtGui import QPixmap
#ADD IMPORT STATEMENT FOR YOUR GENERATED UI.PY FILE HERE
import CountrieOfTheWorld_Lib

#CHANGE THE SECOND PARAMETER HERE TO MATCH YOUR GENERATED UI.PY FILE
class MyForm(QMainWindow, CountrieOfTheWorld_Lib.Ui_MainWindow):
    # declare global variables
    countryList = []
    area = 0
    population = 0
    worldPopulation = 0
    radioButton = 0
    unsavedChanges = False

        # DO NOT MODIFY THIS CODE
    def __init__(self, parent=None):
        super(MyForm, self).__init__(parent)
        self.setupUi(self)
        # END DO NOT MODIFY

        # ADD SLOTS HERE
        self.listWidgetCountries.currentRowChanged.connect(self.List_RowChanged)
        self.actionLoad_Countries.triggered.connect(self.Action_Clicked)
        self.radioButtonPerSquareKM.clicked.connect(self.DensityByKM_Clicked)
        self.radioButtonPerSquareMile.clicked.connect(self.DensityByMiles_Clicked)
        self.pushButtonUpdatePopulation.clicked.connect(self.UpdateButton_Clicked)
        # hidden labels
        self.frameHide.hide()

    # ADD SLOT FUNCTIONS HERE
    def List_RowChanged(self, newIndex):
        self.frameHide.show()
        self.labelTitleCountryName.setText(self.countryList[newIndex][0])
        self.textEditDisPopulation.setText(self.countryList[newIndex][1])
        self.labelDisArea.setText(self.countryList[newIndex][2])

        # Display flag
        countryName = self.countryList[newIndex][0]
        countryName = countryName.replace(" ", "_")
        file = "Flags\\" + countryName
        self.labelDisFlag.setPixmap(QPixmap(file))

        # store population and area outside of function
        self.population = self.countryList[newIndex][1]
        self.area = self.countryList[newIndex][2]

        # check to see which radio button is clicked to correctly display density by default
        if self.radioButton == 0:
            self.DensityByMiles_Clicked(self)
        else:
            self.DensityByKM_Clicked(self)

        # calculate world population
        for row in self.countryList:
            addition = row[1]
            self.worldPopulation += int(addition)
        # display percentage of world population
        popPercent = (int(self.population) / self.worldPopulation) * 100
        self.labelDisPercentOfWorld.setText(str(round(popPercent,4)) + "%")

    def Action_Clicked(self):
        self.LoadCountriesFromFile()
        self.LoadCountriesIntoWidget()

    def DensityByKM_Clicked(self, enabled):
        if enabled:
            density = int(self.population) / (int(self.area) * 2.58999)
            self.labelDisPopulationDensity.setText(str(round(density, 3)))
        # set variable radio button so the default calculation is correct
        self.radioButton = 1

    def DensityByMiles_Clicked(self, enabled):
        if enabled:
            density = int(self.population) / int(self.area)
            self.labelDisPopulationDensity.setText(str(round(density, 3)))
        # set variable radio button so the default calculation is correct
        self.radioButton = 0


    # when Update Button is clicked
    def UpdateButton_Clicked(self):
        self.SaveToMemory()
        self.unsavedChanges = True


    # ADD HELPER FUNCTIONS HERE
    def LoadCountriesFromFile(self):
        with open("countries.txt", "r") as myFile:
            theData = csv.reader(myFile)

            self.countryList = []
            for row in theData:
                self.countryList.append(row)

    def LoadCountriesIntoWidget(self):
        self.listWidgetCountries.clear()
        for country in  self.countryList:
            self.listWidgetCountries.addItem(country[0])

    def ConvertMilesToKilometers(miles):
        kilometers = miles * 2.58999
        return  kilometers


    # to save into memory
    def SaveToMemory(self):

        # Ask the widget for index of the current row
        selectedIndex = self.listWidgetCountries.currentRow()

        # get the user entered population
        pop = self.textEditDisPopulation.toPlainText()

        # set the population in the list to the new population
        self.countryList[selectedIndex][1] = pop

        self.LoadCountriesIntoWidget()

        self.listWidgetCountries.setCurrentRow(selectedIndex)


# DO NOT MODIFY THIS CODE
if __name__ == "__main__":
    app = QApplication(sys.argv)
    the_form = MyForm()
    the_form.show()
    sys.exit(app.exec_())
# END DO NOT MODIFY
