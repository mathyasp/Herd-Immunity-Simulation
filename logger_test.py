from simulation import Simulation
from person import Person
from logger import Logger
from virus import Virus

if __name__ == '__main__':
    file_name = 'test_logger_file.txt'
    virus_name = 'Sniffles'
    repro_num = 0.5
    mortality_rate = 0.12
    pop_size = 1000
    vacc_percentage = 0.1
    initial_infected = 10

    new_logger = Logger(file_name)

    assert new_logger.file_name == 'test_logger_file.txt'


    # Test log file was created + test write_metadata method 
    new_logger.write_metadata(pop_size, vacc_percentage, virus_name, mortality_rate, repro_num, initial_infected)

    file = open('test_logger_file.txt', 'r')
    write_test = file.read()


    # Test log_interactions method
    new_logger.log_interactions(10, 5)

    file = open('test_logger_file.txt', 'r')
    interactions_test = file.read()


    # Test log_infection_survival method
    new_logger.log_infection_survival(100, 5, 10)

    file = open('test_logger_file.txt', 'r')
    infection_survival_test = file.read()


    # Test log_time_step method
    new_logger.log_time_step(1)

    file = open('test_logger_file.txt', 'r')
    time_step_test = file.read()


    # Test log_final_stats method
    new_logger.log_final_stats(100, 5, 10, 'Everyone died', 100, 10, 20, 1000, 40)

    file = open('test_logger_file.txt', 'r')
    final_stats_test = file.read()


    # Test that the log file is correct
    assert final_stats_test == 'Population Size: 1000\nVaccination Percentage: 0.1\nVirus Name: Sniffles\nMortality Rate: 0.12\nBasic Reproduction Number: 0.5\nDate of Simulation: 10\n\nNumber of New Infections: 10\nNumber of New Deaths: 5\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\nCurrent Population Count: 100\nTotal Number of Deaths: 5\nTotal Number of Vaccinations Administered: 10\n\n\n\n\n----------------------------\nTime Step Number: 1\n----------------------------\n-~-~-~-~-~-~-~-~-~-~-~-~-~-\n\nNumber of Survivors: 100\nTotal Number of Deaths: 5\nTotal Number of Vaccinations: 10\nReason for Simulation Ending: Everyone died\nTotal Number of Interactions: 100\nNewly Vaccinated Count: 10\nPerecentage of Population That Became Infected: 2.0%\nPerecentage of Population That Died: 0.5%\nNumber of Lives Saved by Vaccinations: 40\n'