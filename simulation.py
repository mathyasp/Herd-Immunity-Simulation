import random, sys, math
# random.seed(42)
from person import Person
from logger import Logger
from virus import Virus


class Simulation(object):
    def __init__(self, virus, pop_size, vacc_percentage, initial_infected=1):
        # TODO: Create a Logger object and bind it to self.logger.
        # Remember to call the appropriate logger method in the corresponding parts of the simulation.
        self.logger = Logger(f"{virus.name}-logfile.txt")
        
        # TODO: Store the virus in an attribute
        self.virus = virus
        # TODO: Store pop_size in an attribute
        self.pop_size = pop_size
        # TODO: Store the vacc_percentage in a variable
        self.vacc_percentage = vacc_percentage
        # TODO: Store initial_infected in a variable
        self.initial_infected = initial_infected
        # You need to store a list of people (Person instances)
        # Some of these people will be infected some will not. 
        # Use the _create_population() method to create the list and 
        # return it storing it in an attribute here. 
        # TODO: Call self._create_population() and pass in the correct parameters.
        self.initial_vaccination_count = math.floor(self.pop_size * self.vacc_percentage)
        self.population = self._create_population()
        self.vaccination_count = 0
        self.time_step_counter = 0
        self.newly_infected = []
        self.interaction_count = 0
        self.new_fatality_count = 0


    def _create_population(self):
        # TODO: Create a list of people (Person instances). This list 
        # should have a total number of people equal to the pop_size. 
        # Some of these people will be uninfected and some will be infected.
        # The number of infected people should be equal to the the initial_infected
        # TODO: Return the list of people
        population_list = []

        for i in range(1, self.pop_size + 1):
            population_list.append(Person(i, False))
        for i in range(0, (self.initial_vaccination_count)):
            population_list[i].is_vaccinated = True
        for i in range(0, (self.initial_infected)):
            population_list[i].infection = self.virus
        return population_list
        

    def _simulation_should_continue(self):
        # This method will return a booleanb indicating if the simulation 
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

        should_continue = True

        while should_continue:
            # TODO: Increment the time_step_counter
            self.time_step_counter += 1
            # TODO: for every iteration of this loop, call self.time_step() 
            self.time_step()
            # Call the _simulation_should_continue method to determine if 
            # the simulation should continue
            should_continue = self._simulation_should_continue()

        # TODO: Write meta data to the logger. This should be starting 
        # statistics for the simulation. It should include the initial
        # population size and the virus. 
        self.logger.write_metadata(self.pop_size, self.vacc_percentage, self.virus.name, self.virus.mortality_rate, self.virus.repro_rate)
        
        # TODO: When the simulation completes you should conclude this with 
        # the logger. Send the final data to the logger. 
        survivor_count = 0
        infected_count = 0
        fatality_count = 0
        for person in self.population:
            if person.is_alive:
                survivor_count += 1
            else:
                fatality_count += 1
            if person.infection != None:
                infected_count += 1

        newly_infected_count = infected_count - self.initial_infected
        new_vaccinated_count = self.vaccination_count - self.initial_vaccination_count

        self.logger.log_final_stats(survivor_count, fatality_count, infected_count, self.vaccination_count, self.interaction_count, newly_infected_count, new_vaccinated_count)


    def time_step(self):
        # This method will simulate interactions between people, calulate 
        # new infections, and determine if vaccinations and fatalities from infections
        # The goal here is have each infected person interact with a number of other 
        # people in the population
        # TODO: Loop over your population
        # For each person if that person is infected
        # have that person interact with 100 other living people 
        # Run interactions by calling the interaction method below. That method
        # takes the infected person and a random person
        for person in self.population:
            if person.infection != None and person.is_alive:
                for i in range(0, 100):
                    random_person = random.choice(self.population)
                    while not random_person.is_alive:
                        random_person = random.choice(self.population)
                    self.interaction_count += 1
                    self.interaction(person, random_person)
        self._infect_newly_infected()


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
        if random_person.infection == None and not random_person.is_vaccinated:
            if random.random() < self.virus.repro_rate:
                self.newly_infected.append(random_person)
        self.logger.log_interactions(self.time_step_counter, self.interaction_count, len(self.newly_infected))


    def _infect_newly_infected(self):
        # TODO: Call this method at the end of every time step and infect each Person.
        # TODO: Once you have iterated through the entire list of self.newly_infected, remember
        # to reset self.newly_infected back to an empty list.
        for person in self.newly_infected:
            person.infection = self.virus
            if person.did_survive_infection():
                self.vaccination_count += 1
                person.is_vaccinated = True
            else:
                person.is_alive = False
                self.new_fatality_count += 1
        self.newly_infected = []


if __name__ == "__main__":
    # Test your simulation here
    virus_name = "Sniffles"
    repro_num = 0.5
    mortality_rate = 0.12

    # Set some values used by the simulation
    pop_size = 1000
    vacc_percentage = 0.1
    initial_infected = 10

    # Make a new instance of the simulation
    virus = Virus(virus_name, repro_num, mortality_rate)
    sim = Simulation(virus, pop_size, vacc_percentage, initial_infected)

    sim.run()
