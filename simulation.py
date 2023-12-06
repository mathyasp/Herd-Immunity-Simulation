import random, sys, math, argparse
import matplotlib.pyplot as plt
# random.seed(42)
from datetime import date
sys.path.append('../classes/')
from person import Person
from logger import Logger
from virus import Virus


class Simulation(object):
    def __init__(self, virus, pop_size, vacc_percentage, initial_infected=1):
        # TODO: Create a Logger object and bind it to self.logger.
        # Remember to call the appropriate logger method in the corresponding parts of the simulation.
        self.logger = Logger(f'./logs/{virus.name}_log_file.txt')
        
        # TODO: Store the virus in an attribute
        self.virus = virus
        # TODO: Store pop_size in an attribute
        self.pop_size = pop_size
        # TODO: Store the vacc_percentage in a variable
        self.vacc_percentage = vacc_percentage
        self.initial_vaccination_count = math.floor(self.pop_size * (self.vacc_percentage/100))
        self.array_of_infected = []
        # TODO: Store initial_infected in a variable
        self.initial_infected = initial_infected
        # You need to store a list of people (Person instances)
        # Some of these people will be infected some will not. 
        # Use the _create_population() method to create the list and 
        # return it storing it in an attribute here. 
        # TODO: Call self._create_population() and pass in the correct parameters.
        self.population = self._create_population()
        self.vaccination_count = 0
        self.newly_infected = []
        self.newly_dead = []
        self.interaction_count = 0
        self.vaccine_saves = 0
        # Matplotlib arrays
        self.infections_plot_values = [self.initial_infected]
        self.deaths_plot_values = [0]
        self.vaccinations_plot_values = [self.initial_vaccination_count]
        self.pop_size_plot_values = [self.pop_size]


    def _create_population(self):
        # TODO: Create a list of people (Person instances). This list 
        # should have a total number of people equal to the pop_size. 
        # Some of these people will be uninfected and some will be infected.
        # The number of infected people should be equal to the the initial_infected
        # TODO: Return the list of people
        population_list = []

        for i in range(0, self.pop_size):
            population_list.append(Person(i, False))
        for i in range(0, (self.initial_vaccination_count)):
            population_list[i].is_vaccinated = True
        for i in range(0, (self.initial_infected)):
            population_list[i].infection = self.virus
        return population_list
        

    def _simulation_should_continue(self):
        # This method will return a boolean indicating if the simulation 
        # should continue. 
        # The simulation should not continue if all of the people are dead, 
        # or if all of the living people have been vaccinated. 
        # TODO: Loop over the list of people in the population. Return True
        # if the simulation should continue or False if not.
        for person in self.population:
            if person.is_alive and not person.is_vaccinated:
                return True
        return False

    def run(self):
        # This method starts the simulation. It should track the number of 
        # steps the simulation has run and check if the simulation should 
        # continue at the end of each step. 

        # TODO: Write meta data to the logger. This should be starting 
        # statistics for the simulation. It should include the initial
        # population size and the virus. 
        self.logger.write_metadata(self.pop_size, self.vacc_percentage, self.virus.name, self.virus.mortality_rate, self.virus.repro_rate, date.today().strftime('%Y-%m-%d'))

        time_step_counter = 0
        should_continue = True

        while should_continue:
            # TODO: Increment the time_step_counter
            time_step_counter += 1
            # TODO: for every iteration of this loop, call self.time_step() 
            self.time_step(time_step_counter)
            # Call the _simulation_should_continue method to determine if 
            # the simulation should continue
            should_continue = self._simulation_should_continue()
        
        # TODO: When the simulation completes you should conclude this with 
        # the logger. Send the final data to the logger. 
        fatality_count = len(self.population) - self.pop_size
        infected_count = 0

        for person in self.population:
            if person.infection != None:
                infected_count += 1

        newly_infected_count = infected_count - self.initial_infected
        total_vaccination_count = self.vaccination_count + self.initial_vaccination_count
        reason_for_ending = 'The entire population has died.' if fatality_count == len(self.population) else 'All living people have been vaccinated.'
        self.logger.log_final_stats(self.pop_size, fatality_count, total_vaccination_count, reason_for_ending, self.interaction_count, self.vaccination_count, newly_infected_count, len(self.population), self.vaccine_saves)
        self.plot_simulation_results()


    def time_step(self, time_step_counter):
        # This method will simulate interactions between people, calulate 
        # new infections, and determine if vaccinations and fatalities from infections
        # The goal here is have each infected person interact with a number of other 
        # people in the population
        # TODO: Loop over your population
        # For each person if that person is infected
        # have that person interact with 100 other living people 
        # Run interactions by calling the interaction method below. That method
        # takes the infected person and a random person
        self.logger.log_time_step(time_step_counter)
        for person in self.population:
            if person.infection != None and person.is_alive:
                for i in range(0, 100):
                    random_person = random.choice(self.population)
                    while not random_person.is_alive:
                        random_person = random.choice(self.population)
                    self.interaction(person, random_person)
        self._infect_newly_infected()
        fatality_count = len(self.population) - self.pop_size
        self.logger.log_interactions(len(self.newly_infected), len(self.newly_dead))
        # Append the values to the plot arrays
        self.infections_plot_values.append(self.infections_plot_values[-1] + len(self.newly_infected))
        self.deaths_plot_values.append(fatality_count)
        self.vaccinations_plot_values.append(self.vaccination_count)
        self.pop_size_plot_values.append(self.pop_size)
        # Clear tracking arrays and log the infection survival
        self.newly_infected = []
        self.newly_dead = []
        self.logger.log_infection_survival(self.pop_size, fatality_count, self.vaccination_count)


    def interaction(self, infected_person, random_person):
        # TODO: Finish this method.
        # The possible cases you'll need to cover are listed below:
        # random_person is vaccinated:
        #     nothing happens to random person.
        # random_person is already infected:
        #     nothing happens to random person.
        # random_person is healthy, but unvaccinated:
        #     generate a random number between 0.0 and 1.0.  If that number is smaller
        #     than repro_rate, add that person to the newly infected array
        #     Simulation object's newly_infected array, so that their infected
        #     attribute can be changed to True at the end of the time step.
        # TODO: Call logger method during this method.
        self.interaction_count += 1
        if random_person.infection is None and not random_person.is_vaccinated:
            if random.random() < self.virus.repro_rate:
                self.newly_infected.append(random_person)

        # The instructions technically say to make log here, however this makes the text file massive/infinite
            # Code left as comment intentionally
        # self.logger.log_interactions(len(self.newly_infected), len(self.newly_dead))
        # self.newly_dead = []
        # self.newly_infected = []


    def _infect_newly_infected(self):
        # TODO: Call this method at the end of every time step and infect each Person.
        # TODO: Once you have iterated through the entire list of self.newly_infected, remember
        # to reset self.newly_infected back to an empty list.
        for person in self.newly_infected:
            person.infection = self.virus
            if person.did_survive_infection():
                self.vaccination_count += 1
                person.is_vaccinated = True
                self.vaccine_saves += 1
            else:
                person.is_alive = False
                self.pop_size -= 1
                self.newly_dead.append(person)


    def plot_simulation_results(self):
        # Plot infections
        plt.plot(self.infections_plot_values, label='Infections')

        # Plot deaths
        plt.plot(self.deaths_plot_values, label='Deaths')

        # Plot vaccinations
        plt.plot(self.vaccinations_plot_values, label='Vaccinations')

        # Plot population size
        plt.plot(self.pop_size_plot_values, label='Population Size')

        # Add labels and title
        plt.xlabel('Time Step')
        plt.ylabel('Count')
        plt.title('Herd Immunity Simulation')

        # Add legend
        plt.legend()

        # Show the plot
        plt.show()
        # Plot infections
        plt.plot(self.infections_plot_values, label='Infections')

        # Plot deaths
        plt.plot(self.deaths_plot_values, label='Deaths')

        # Plot vaccinations
        plt.plot(self.vaccinations_plot_values, label='Vaccinations')

        # Plot population size
        plt.plot(self.pop_size_plot_values, label='Population Size')

        # Add labels and title
        plt.xlabel('Time Step')
        plt.ylabel('Count')
        title_name = f'Herd Immunity Simulation - {virus.name}'
        plt.title(title_name)  

        # Add legend
        plt.legend()

        # Show the plot
        plt.show()


if __name__ == '__main__':
    # Test your simulation here
    # virus_name = 'Sniffles'
    # repro_num = 0.5
    # mortality_rate = 0.12

    # Set some values used by the simulation
    # pop_size = 1000
    # vacc_percentage = 10
    # initial_infected = 10

    # To enable CLI inputs
    parser = argparse.ArgumentParser()
    parser.add_argument('pop_size', metavar='pop_size', type=int, help='Population size as integer')
    parser.add_argument('vacc_percentage', metavar='vacc_percentage', type=float, help='Vaccination percentage as float')
    parser.add_argument('virus_name', metavar='virus_name', type=str, help='Virus name as string')
    parser.add_argument('mortality_rate', metavar='mortality_rate', type=float, help='Mortality rate as float')
    parser.add_argument('repro_num', metavar='repro_num', type=float, help='Reproduction number as float')
    parser.add_argument('initial_infected', metavar='initial_infected', type=int, help='Intially infected as integer')
    args = parser.parse_args()
    
    virus_name = args.virus_name
    repro_num = args.repro_num
    mortality_rate = args.mortality_rate
    pop_size = args.pop_size
    vacc_percentage = args.vacc_percentage
    initial_infected = args.initial_infected

    # Make a new instance of the simulation
    virus = Virus(virus_name, repro_num, mortality_rate)
    sim = Simulation(virus, pop_size, vacc_percentage, initial_infected)

    sim.run()
