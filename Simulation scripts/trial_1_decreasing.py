# needed to run this example without prior
# installation of DOSE into Python site-packages
try: 
    import run_examples_without_installation
except ImportError: pass

# Example codes starts from here
import copy
import os
import random
import sys

import dose
from dose_interpreters import D2

environmental_data = [1000, # metabolite A / 0 (importer)
                      500, # metabolite B / 1
                      692, # metabolite C / 2 (importer)
                      500, # metabolite D / 3
                      479, # metabolite E / 4 (importer)
                      500, # metabolite F / 5
                      332, # metabolite G / 6 (importer)
                      500, # metabolite H / 7
                      230, # metabolite I / 8 (importer)
                      500, # metabolite J / 9
                      159, # metabolite K / 10 (importer)
                      500, # metabolite L / 11
                      110, # metabolite M / 12 (importer)
                      500, # metabolite N / 13
                      76, # metabolite O / 14 (importer)
                      500, # metabolite P / 15
                      53, # metabolite Q / 16 (importer)
                      500, # metabolite R / 17
                      36, # metabolite S / 18 (importer)
                      500, # metabolite T / 19
                      25, # metabolite U / 20 (importer)
                      500, # metabolite V / 21
                      17, # metabolite W / 22 (importer)
                      500, # metabolite X / 23
                      12   # metabolite Y / 24 (importer)
                     ]

parameters = {# Part 1: Simulation metadata
              "simulation_name": "trial_1_decreasing",
              "population_names": ['pop_01'],

              # Part 2: World settings
              "world_x": 3,
              "world_y": 3,
              "world_z": 1,
              "population_locations": [[(0,0,0)]],
              "eco_cell_capacity": 100,
              "deployment_code": 1,

              # Part 3: Population settings
              "population_size": 100,

              # Part 4: Genetics settings
              "genome_size": 1,
              "chromosome_size": 700,
              "chromosome_bases": ['01', '02', '03', '04', '05', 
                                   '06', '07', '08', '09', '10',
                                   '11', '12', '13', '14', '15',
                                   '16', '17', '18', '19', '20',
                                   '21', '22', '23', '24', '25',
                                   '26', '27', '28', '29', '30',
                                   '31', '32', '33', '34', '35',
                                   '36', '37', '38', '39', '40',
                                   '41', '42', '43', '44', '45',
                                   '46', '47', '48', '49', '50',
                                   '51', '52', '53', '54', '55',
                                   '56', '57', '58', '59', '60',
                                   '61', '62', '63', '64', '65',
                                   '66', '67', '68', '69', '70'],
              "initial_chromosome": ['01', '02', '03', '04', '05', 
                                   '06', '07', '08', '09', '10',
                                   '11', '12', '13', '14', '15',
                                   '16', '17', '18', '19', '20',
                                   '21', '22', '23', '24', '25',
                                   '26', '27', '28', '29', '30',
                                   '31', '32', '33', '34', '35',
                                   '36', '37', '38', '39', '40',
                                   '41', '42', '43', '44', '45',
                                   '46', '47', '48', '49', '50',
                                   '51', '52', '53', '54', '55',
                                   '56', '57', '58', '59', '60',
                                   '61', '62', '63', '64', '65',
                                   '66', '67', '68', '69', '70'] * 10,

              # Part 5: Mutation settings
              "background_mutation": 0.01,
              "additional_mutation": 0,
              "mutation_type": 'point',
              
              # Part 6: Metabolic settings
              "interpreter": D2.interpreter,
              "instruction_size": 2,
              "ragaraja_version": "user-defined",
              "base_converter": None,
              "ragaraja_instructions": [],
              "max_tape_length": 25,
              "interpret_chromosome": True,
              "clean_cell": True,
              "max_codon": 2000,

              # Part 7: Simulation settings
              "goal": 0,
              "maximum_generations": 1500,
              "eco_buried_frequency": 100,
              "fossilized_ratio": 0.01,
              "fossilized_frequency": 20,
              
              # Part 8: Simulation report settings
              "print_frequency": 50,
              "database_file": "d2.db",
              "database_logging_frequency": 50
             }

class simulation_functions(dose.dose_functions):

    def organism_movement(self, Populations, pop_name, World): pass

    def organism_location(self, Populations, pop_name, World): pass

    def ecoregulate(self, World): pass

    def update_ecology(self, World, x, y, z): pass

    def update_local(self, World, x, y, z): pass

    def report(self, World): pass

    def fitness(self, Populations, pop_name): 
        for organism in Populations[pop_name].agents:
            organism.status['fitness'] = \
                sum(organism.status['blood']) / len(organism.status['blood'])

    def mutation_scheme(self, organism): 
        organism.genome[0].rmutate(parameters["mutation_type"],
                                   parameters["additional_mutation"])

    def prepopulation_control(self, Populations, pop_name):
        agents = Populations[pop_name].agents
        status = [(index, agents[index].status['fitness'])
                   for index in range(len(agents))]
        eliminate = [x[1] for x in status]
        eliminate.sort()
        ethreshold = eliminate[9]
        if len([x for x in eliminate if x > ethreshold]) < 50:
            eliminate = [x[0] for x in status]
            eliminate = [random.choice(eliminate) for x in range(10)]
            Populations[pop_name].agents = \
                [agents[i] for i in range(len(agents))
                    if i not in eliminate]
        print("Population size after elimination: " + \
            str(len(Populations[pop_name].agents)))

    def mating(self, Populations, pop_name): 
        agents = Populations[pop_name].agents
        while len(agents) < 100:
            chosen_agent = random.choice(agents)
            new_agent = copy.deepcopy(chosen_agent)
            new_agent.status['parents'] = new_agent.status['identity']
            new_agent.generate_name()
            agents.append(new_agent)

    def postpopulation_control(self, Populations, pop_name): pass

    def generation_events(self, Populations, pop_name): pass

    def population_report(self, Populations, pop_name):
        for org in Populations[pop_name].agents:
            generation = org.status['generation']
            fitness = str(org.status['fitness'])
            blood = ','.join([str(m) for m in org.status['blood']])
            if (generation == 1) or (generation % parameters["print_frequency"]) == 0:
                print(",".join([str(generation), str(fitness), str(blood)]))
        return Populations

    def database_report(self, con, cur, start_time, 
                        Populations, World, generation_count):
        try:
            dose.database_report_populations(con, cur, start_time, 
                                             Populations, generation_count)
        except: pass
        try:
            dose.database_report_world(con, cur, start_time, 
                                       World, generation_count)
        except: pass

    def deployment_scheme(self, Populations, pop_name, World): pass


if __name__ == "__main__":
    if len(sys.argv) == 2: 
        parameters["simulation_name"] = sys.argv[1]
    print('\n[' + parameters["simulation_name"].upper() + ' SIMULATION]')
    print('Adding deployment scheme to simulation parameters...')
    parameters["deployment_scheme"] = simulation_functions.deployment_scheme
    print('Constructing World entity...')
    World = dose.dose_world.World(parameters["world_x"],
                             parameters["world_y"],
                             parameters["world_z"])
    dose.load_all_local_input(World, environmental_data)
    print('Spawning populations...')
    Populations = dose.spawn_populations(parameters)
    print('\nStarting simulation on sequential ecological cell simulator...')
    (simulation_functions, parameters, Populations, World) = \
        dose.sequential_simulator(simulation_functions, parameters, 
                                  Populations, World)
    print('\nSimulation ended...')
    