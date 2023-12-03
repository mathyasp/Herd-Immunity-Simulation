
class Logger(object):
    def __init__(self, file_name):
        self.file_name = file_name

    def write_metadata(self, pop_size, vacc_percentage, virus_name, mortality_rate, basic_repro_num):
        # TODO: Finish this method. This line of metadata should be tab-delimited
        # it should create the text file that we will store all logs in.
        # TIP: Use 'w' mode when you open the file. For all other methods, use
        # the 'a' mode to append a new log to the end, since 'w' overwrites the file.
        # NOTE: Make sure to end every line with a '/n' character to ensure that each
        # event logged ends up on a separate line!
        log = open(self.file_name, "w")
        log.write(f'Population Size: {pop_size}\n'
                        f'Vaccination Percentage: {vacc_percentage}\n'
                        f'Virus Name: {virus_name}\n'
                        f'Mortality Rate: {mortality_rate}\n'
                        f'Basic Reproduction Number: {basic_repro_num}\n')
        log.close()

    def log_interactions(self, step_number, number_of_interactions, number_of_new_infections):
        # TODO: Finish this method. Think about how the booleans passed (or not passed)
        # represent all the possible edge cases. Use the values passed along with each person,
        # along with whether they are sick or vaccinated when they interact to determine
        # exactly what happened in the interaction and create a String, and write to your logfile.
        log = open(self.file_name, "a")
        log.write(f'\nStep Number: {step_number}\n'
                            f'New Interaction Count: {number_of_interactions}\n'
                            f'New Infection Count: {number_of_new_infections}\n')
        log.close()

    def log_infection_survival(self, step_number, population_count, number_of_new_fatalities):
        # TODO: Finish this method. If the person survives, did_die_from_infection
        # should be False.  Otherwise, did_die_from_infection should be True.
        # Append the results of the infection to the logfile
        log = open(self.file_name, "a")
        log.write(f'\nStep Number: {step_number}\n'
                            f'Current Population Count: {population_count}\n'
                            f'New Fatality Count: {number_of_new_fatalities}\n')
        log.close()


    def log_time_step(self, time_step_number):
        # 
        log = open(self.file_name, "a")
        log.write(f'\nTime Step Number: {time_step_number}\n')
        log.close()


    def log_final_stats(self, surivor_count, fatality_count, total_infected_count, total_vaccinated_count, interaction_count, new_infected_count, new_vaccinated_count):
        log = open(self.file_name, "a")
        log.write(f'\nSurvivor Count: {surivor_count}\n'
                            f'Fatality Count: {fatality_count}\n'
                            f'Total Infected Count: {total_infected_count}\n'
                            f'Total Vaccinated Count: {total_vaccinated_count}\n'
                            f'Interaction Count: {interaction_count}\n'
                            f'New Infection Count: {new_infected_count}\n'
                            f'Newly Vaccinated Count: {new_vaccinated_count}\n')
        log.close()
