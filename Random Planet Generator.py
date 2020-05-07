
#   === INFO ===
# This program is meant to be a very accurate planet generator. Obviously, there are some things that are missing
# as it is impossible to add every physical phenomena to such a program.
# Here is a list of the things that have been left out, either because it will make the code a lot simpler, or
# they would not add much to the program :
#
#  - All hyper-giant, super-giant, and giant stars (except for red giants) were not included as they are far too rare.
#  - Blue stars were also not included due to their incredible rarity and short lifespan.
#  - binary systems from protobinary systems were not fully implemented to keep code simple. To compensate, the
#    frequency of binary systems was reduced.
#  - The frequency of compounds found on exoplanets may not be fully accurate, as not much is known about the
#    substances on exoplanets due to them being extremely difficult to detect.
#  - Elliptical orbits are not visualized in the orbital visual. Moons/planets with a relatively large periods
#    will often have elliptical orbits.
#  - The colour of planets does not rely on the compounds beneath as there is no formula to
#    gather the colour of compounds; each compound colour is reliant on dozens of complex factors.
#  - Density of exoplanets was averaged out as true density relies on far too many factors for a guy in high
#    school to account for.
#  - Giant planet moon rate was reduced by about a factor of 10, as the moons cause too much lag.
#  - Hardly anything is known about exoplanet atmospheres, and there is not much confirmed knowledge about them hence
#    why this program does not go into depth about atmospheres.



import arcade
import math
import random

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800

CENTER_X = SCREEN_WIDTH / 4 * 2.9   # center of orbital window
CENTER_Y = (SCREEN_HEIGHT / 4 * 2.85)-25  # center of orbital window

CENTER_X_MAGNIFIED = SCREEN_WIDTH / 4 * 2.9
CENTER_Y_MAGNIFIED = (SCREEN_HEIGHT / 4 * 2.85) - (SCREEN_HEIGHT/2)

MAGNIFIED_LENGTH = SCREEN_WIDTH // 3
MAGNIFIED_HEIGHT = SCREEN_HEIGHT // 3

ASTRONOMICAL_UNIT = 1.496 * (10**11)

IN = "0123456789"
OU = "₀₁₂₃₄₅₆₇₈₉"
SUB = str.maketrans(IN, OU)

PI = 3.14159

PI2 = PI/2

TICK = 2*PI/60  # Means that every second the orbitals in the orbital visual window will complete an orbit, assuming
#                 that there is no modification to sin or cos curve.

TICK_RATE = 15768000  # The amount of seconds that will pass with each tick in orbital visual window.

GRAVITY_CONSTANT = 6.67408 * (10**-11)
# ALL UNITS IN SI UNITS

STEFAN_BOLTZMANN_CONSTANT = 5.67051 * (10**-8)
# ALL UNITS IN SI UNITS

BOLTZMANN_CONSTANT = 1.38064852 * (10**-23)
# Ironically, this is an entirely different constant than the one above, and was even derived by a different Boltzmann.

SOLAR_MASS = 1.989 * (10**30)
# ALL UNITS IN SI UNITS

EARTH_MASS = 5.972 * (10**24)
# ALL UNITS IN SI UNITS

EXTRA_MASS = 1.024 * (10**26)
# ALL UNITS IN SI UNITS.

EARTH_ORBIT = 150000000000
# ALL UNITS IN SI UNITS

SOLAR_LUMINOSITY = 3.828 * (10**26)
# ALL UNITS IN SI UNITS

EXOPLANET_AVERAGE_DENSITY = 2750
# IN  KG/M^3

"""     ALL UNITS USE SI UNITS EXCEPT DENSITY    """


class Data:  # Stores and creates all data about planets, moons and stars.
    def __init__(self):
        self.p_type = "Super-Earth"  # Not used yet; may be used in future versions.
        self.p_mass = EARTH_MASS  # planet mass
        self.p_atmosphere_pressure = 0  # planet's atmosphere pressure
        self.p_atmosphere_type = []  # planet's atmosphere composition
        self.p_surface_materials = []  # most common surface materials on the planet
        self.p_surface_materials_named = []  # common surface materials named
        self.p_temperature = 0  # Temperature of surface on planet
        self.p_radius = 0  # Radius of planet
        self.p_star_distance = EARTH_ORBIT  # Distance planet is from star
        self.p_colour = (0, 150, 150)
        self.moon_velocity = []
        self.moon_orbit_distance = []
        self.moon_colours = []  # Colour of moons
        self.star_type_1 = "null"  # Type of star 1
        self.star_type_2 = "null"  # Type of star 2
        self.star_luminosity_l = 0  # Luminosity of star
        self.star_luminosity_2 = 0  # Luminosity of 2nd star
        self.star_mass_1 = 0  # star mass
        self.star_mass_2 = 0  # 2nd star mass
        self.star_barycenter_1 = 0  # distance star is from CoM
        self.star_barycenter_2 = 0  # distance 2nd star is from CoM
        self.star_spectral_type = []  # Spectral type of stars
        self.binary_star_distance = 0  # The distance of the binary star orbit
        self.star_radius_1 = 0  # Radius of star 1
        self.star_radius_2 = 0  # Radius of star 2
        self.bin_orbital_period = 1  # Binary orbital period. Both stars will have same period, just different distance.
        self.p_velocity = 0  # Planet velocity
        self.p_gravity_strength = 0  # Planet's gravity acceleration
        self.pressed = 0  # Tells python what button instance is currently on. I did not end up using this.

        self.binary = 0  # When self.binary = 0, there is no binary star system.

        self.orbit_scale = 0

    def moon_generate(self):

        self.moon_orbit_distance.clear()
        self.moon_velocity.clear()
        self.moon_colours.clear()

        range2 = (self.p_mass//EXTRA_MASS)+1
        moons = random.randint(1, range2)

        if moons > 30:  # To ensure that there cannot be ridiculous numbers of moons, or else it lags.
            moons = random.randint(20, 30)

        colours = [(209, 214, 156), (165, 162, 74), (160, 150, 115), (219, 217, 212), (209, 186, 165), (135, 159, 163),
                   (201, 184, 165), (181, 188, 177)]
        colour_weights = [0.125, 0.1, 0.125, 0.15, 0.125, 0.125, 0.125, 0.125]
        for x in range(moons):

            self.moon_velocity.append(random.randint(2000, 8000))
            # velocity of moon orbit
            self.moon_orbit_distance.append(((GRAVITY_CONSTANT * self.p_mass) / (self.moon_velocity[x])**2))
            # orbit distance of moons
            temp = random.choices(colours, weights=colour_weights, k=1)
            self.moon_colours.append(temp[0])

    def planet_resource_generate(self):
        list.clear(self.p_surface_materials)
        list.clear(self.p_surface_materials_named)
        #  metal bonding elements
        iron_2 = dict(charge=2, name='Ferrous', sym='Fe[II]')
        iron_3 = dict(charge=3, name='Ferric', sym='Fe[III]')
        tin_2 = dict(charge=2, name='Stannous', sym='Sn[II]')
        tin_4 = dict(charge=4, name='Stannic', sym='Sn[IV]')
        chromium_2 = dict(charge=2, name='Chromous', sym='Cr[II]')
        chromium_3 = dict(charge=3, name='Chromic', sym='Cr[III]')
        silicon = dict(charge=4, name='Silicon', sym='Si')
        potassium = dict(charge=1, name='Potassium', sym='K')
        magnesium = dict(charge=2, name='Magnesium', sym='Mg')
        calcium = dict(charge=2, name='Calcium', sym='Ca')
        aluminium = dict(charge=3, name='Aluminium', sym='Al')
        lithium = dict(charge=1, name='Lithium', sym='Li')
        sodium = dict(charge=1, name='Sodium', sym='Na')
        copper_2 = dict(charge=2, name='Cupric', sym='Cu[II]')
        copper_1 = dict(charge=1, name='Cuprous', sym='Cu')
        zinc = dict(charge=2, name='Zinc', sym='Zn')
        mercury = dict(charge=2, name='Mercury', sym='Hg')
        tungsten = dict(charge=6, name='Tungsten', sym='W')
        scandium = dict(charge=3, name='Scandium', sym='Sc')
        antimony = dict(charge=5, name='Antimony', sym='Sb')
        ammonium = dict(charge=1, name='Ammonium', sym='(NH4)')

        #  non-metal bonding elements + complex ions
        hydroxide = dict(charge=1, name='hydroxide', sym='(OH)')
        oxide = dict(charge=2, name='oxide', sym='O')
        peroxide = dict(charge=2, name='peroxide', sym='O2')
        nitrate = dict(charge=1, name='nitrate', sym='(NO3)')
        nitride = dict(charge=3, name='nitride', sym='N')
        sulfate = dict(charge=2, name='sulfate', sym='(SO4)')
        chloride = dict(charge=1, name='chloride', sym='Cl')
        iodide = dict(charge=1, name='iodide', sym='I')
        arsenate = dict(charge=3, name='arsenate', sym='(AsO4)')
        borate = dict(charge=3, name='borate', sym='(BO3)')
        chlorite = dict(charge=2, name='chlorite', sym='(ClO2)')
        formate = dict(charge=1, name='formate', sym='(CHO2)')
        dihydrogen_phosphate = dict(charge=1, name='di-hydrogen phosphate', sym='(H2PO4)')
        oxalate = dict(charge=2, name='oxalate', sym='(C2O4)')
        hypochlorate = dict(charge=1, name='hypochlorate', sym='(ClO)')

        weights_material_selection = [0.6, 0.25, 0.125, 0.025]
        material_selection = [1, 2, 3, 4]
        amount_of_selections = random.choices(material_selection, weights=weights_material_selection, k=1)

        selections = amount_of_selections[0]

        # Cations:
        cations = [iron_2, iron_3, tin_2, tin_4, chromium_2, chromium_3, silicon, potassium, magnesium, calcium,
                   aluminium, lithium, sodium, copper_1, copper_2, zinc, mercury, tungsten, scandium, antimony,
                   ammonium]
        cation_weights = [0.02, 0.03, 0.04, 0.04, 0.05, 0.05, 0.05, 0.03, 0.03, 0.04, 0.03, 0.03, 0.06, 0.03, 0.02,
                          0.04, 0.04, 0.005, 0.035, 0.05, 0.07]

        cation_chosen = random.choices(cations, weights=cation_weights, k=selections)

        # Anions:
        anions = [hydroxide, oxide, peroxide, nitrate, nitride, sulfate, chloride, iodide, arsenate, borate, chlorite,
                  formate, dihydrogen_phosphate, oxalate, hypochlorate]
        anion_weights = [0.04, 0.4, 0.04, 0.08, 0.3, 0.02, 0.03, 0.05, 0.09, 0.05, 0.05, 0.08, 0.08, 0.08, 0.05]

        anion_chosen = random.choices(anions, weights=anion_weights, k=selections)

        modifier_cation = [0, 0, 0, 0]  # The number of cations in the ion generated, determined by charge
        modifier_anion = [0, 0, 0, 0]  # The number of anions in the ion generated, determined by charge

        # The charge must equate to 0 when cations are bonding with anions, so I made a large assortment of 'if'
        # statements to test for each possible charge set. I then set the number of each cation and anions in the ion
        # equal to the corresponding positions in the 'modifier' lists.
        # One could argue that I could have got the lowest common multiple of the charges instead, but with
        # such low numbers 'if' statements are much more simple. If numbers were bigger, LCM would be better.
        for o in range(selections):
            if cation_chosen[o].get('charge') == anion_chosen[o].get('charge'):
                modifier_anion[o] = 1
                modifier_cation[o] = 1

            elif cation_chosen[o].get('charge') == 1:
                modifier_cation[o] = anion_chosen[o].get('charge')
                modifier_anion[o] = 1

            elif anion_chosen[o].get('charge') == 1:
                modifier_anion[o] = cation_chosen[o].get('charge')
                modifier_cation[o] = 1

            elif cation_chosen[o].get('charge') == 2 and anion_chosen[o].get('charge') == 3:
                modifier_cation[o] = 3
                modifier_anion[o] = 2

            elif cation_chosen[o].get('charge') == 3 and anion_chosen[o].get('charge') == 2:
                modifier_cation[o] = 2
                modifier_anion[o] = 3

            elif cation_chosen[o].get('charge') == 4 and anion_chosen[o].get('charge') == 3:
                modifier_anion[o] = 4
                modifier_cation[o] = 3

            elif cation_chosen[o].get('charge') == 2 * anion_chosen[o].get('charge'):
                modifier_cation[o] = 1
                modifier_anion[o] = 2

            elif cation_chosen[o].get('charge') == 3 * anion_chosen[o].get('charge'):
                modifier_cation[o] = 1
                modifier_anion[o] = 3

            elif cation_chosen[o].get('charge') == 5:
                        if anion_chosen[o].get('charge') == 3:
                                modifier_anion[o] = 5
                                modifier_cation[o] = 3
                        elif anion_chosen[o].get('charge') == 2:
                                modifier_anion[o] = 5
                                modifier_cation[o] = 2

        # This will put together the Ions selected in order, and will also use a .get('name') statement to acquire the
        # names of ion that was generate.
        for n in range(selections):
            t = "{}{}{}{}".format(cation_chosen[n].get('sym'),modifier_cation[n],anion_chosen[n].get('sym'),
                                  modifier_anion[n])
            t.translate(SUB)
            self.p_surface_materials.append(t)
            self.p_surface_materials_named.append('{} {}'.format(cation_chosen[n].get('name'),
                                                  anion_chosen[n].get('name')))

    # NOTE: THIS FUNCTION BLOCK WOULD HAVE BEEN USED BETTER IF THERE WAS AN EASY WAY TO PREDICT THE GREENHOUSE EFFECT
    # ATMOSPHERES HAVE ON EXOPLANET TEMPERATURE.
    # Since exoplanet temperature is extremely low in all cases due to absence of greenhouse effect and lack thereof
    # to calculate it, it is near impossible to determine what state of matter each of the below materials would be in.
    def other_material_generate(self):
        self.p_atmosphere_type.clear()
        hydrogen = dict(bp=-252, mp=-259, name='Hydrogen', gas=True)  # bp stands for boiling point, mp for melt point.
        ammonia = dict(bp=-33, mp=-78, name='Ammonia', gas=False)
        methane = dict(bp=-162, mp=-182, name='Methane', gas=True)
        ethane = dict(bp=-89, mp=-182, name='Ethane', gas=True)
        oxygen = dict(bp=-183, mp=-218, name='Oxygen', gas=True)
        xenon = dict(bp=-108, mp=-111, name='Xenon', gas=False)
        water = dict(bp=100, mp=0, name='Water', gas=False)
        helium = dict(bp=-269, mp=-270, name='Helium', gas=True)
        carbon_dioxide = dict(bp=-79, mp=-79, name='Carbon dioxide', gas=False)  # Carbon dioxide has no liquid state.
        carbon_monoxide = dict(bp=-192, mp=-205, name='Carbon monoxide', gas=True)
        nitrogen = dict(bp=-192, mp=-210, name='Nitrogen', gas=True)
        nitrous_oxide = dict(bp=-88, mp=-91, name='Nitrous oxide (Laughing gas)', gas=False)
        nitrogen_dioxide = dict(bp=21, mp=-9, name='Nitrogen dioxide', gas=False)
        sulfur_trioxide = dict(bp=44, mp=-17, name='Sulfur trioxide', gas=False)
        sulfur_dioxide = dict(bp=-10, mp=-72, name='Sulfur dioxide', gas=False)
        nitrogen_trifluoride = dict(bp=-129, mp=-207, name='Nitrogen trifluoride', gas=True)

        x = random.randint(1, 3)  # The number of gases prevalent on the chosen planet.

        weight = [0.2, 0.05, 0.05, 0.1, 0.02, 0.05, 0.05, 0.05, 0.05, 0.1, 0.05, 0.1, 0.1, 0.1, 0.1, 0.1]
        selections = [hydrogen, methane, ethane, oxygen, xenon, water, helium, carbon_dioxide, carbon_monoxide,
                      nitrogen, nitrous_oxide, sulfur_trioxide, sulfur_dioxide, nitrogen_dioxide, ammonia,
                      nitrogen_trifluoride]

        materials = random.choices(selections, weights=weight, k=x)

        #  calculating what state of matter each substance is in;
        for o in range(x):
            if materials[o].get('bp') < self.p_temperature:
                self.p_atmosphere_type.append(materials[o].get('name'))
            elif materials[o].get('mp') < self.p_temperature:
                self.p_surface_materials.append("Liquid {}".format(materials[o].get('name')))
            else:
                self.p_surface_materials_named.append("{} in solid form".format(materials[o].get('name')))

        # Currently, there is no known way to calculate atmosphere pressure on exoplanets. Scientists must estimate,
        # so I have come up with an equation that satisfies most known exoplanet pressures:
        #  atmosphere pressure = 60 * (gravity_strength)^2
        self.p_atmosphere_pressure = 60 * (self.p_gravity_strength**2)

        last_ditch_gases = ['Carbon dioxide', 'Carbon monoxide', 'Nitrogen trifluoride', 'Methane']
        # If no gas is selected, a random gas will be selected from this list. Often when many planet conditions are
        # unsatisfied for other gases this is the most factual option.

        if self.p_gravity_strength > 2 and len(self.p_atmosphere_type) == 0:  # Testing for atmosphere, in case none.
            j = random.choices(selections, weights=weight, k=1)  # If escape velocity too low, it will not run.
            t = j[0]
            if t.get('gas'):
                self.p_atmosphere_type.append(t.get('name'))  # Will put in the gas, if it is suitable.
            else:
                y = random.choices(last_ditch_gases)
                self.p_atmosphere_type.append(y[0])
        # This set of code is to ensure that no planets are generated without at least a trace of an atmosphere.

        if len(self.p_atmosphere_type) > 1:
            if self.p_atmosphere_type[0] == self.p_atmosphere_type[1]:
                self.p_atmosphere_type.pop()  # Will remove one gas type if there are 2 of the same gases.

    def general_generation(self):
        self.p_radius = random.randint(1592750, 139982000)  # in meters

        self.p_velocity = random.randint(5000, 8000)  # in meters per second

        #  Using Fc = mv^2/r, and Fg = [GRAVITY_CONSTANT]Mm/r^2 we can re-arrange to get:
        #  r = (GM/v^2)^0.5 , which will give planet distance from star in m.
        #  self.star_mass_2 is multiplied by self.binary so if there is no binary system, the second star's mass is
        #  not added.
        self.p_star_distance = GRAVITY_CONSTANT * (self.star_mass_1 + (self.star_mass_2 * self.binary)) \
            / self.p_velocity**2

        self.p_mass = ((4*PI/3) * self.p_radius**3) * EXOPLANET_AVERAGE_DENSITY
        # Using the formula of volume of a sphere, we can deduce mass of exoplanet by multiplying by average density.

        # Using  Fg = [GRAVITY_CONSTANT]Mm/r^2  and  F = ma  we can get  a = [GRAVITY_CONSTANT]M/r^2 which will give
        # acceleration due to the planet's gravity.
        self.p_gravity_strength = (GRAVITY_CONSTANT * self.p_mass) / self.p_radius ** 2

        # Since colour is really REALLY difficult to determine as it relies on hundreds of complex molecular factors,
        # I will just going to randomly generate it. This stuff is too complex for a school lad.
        colour_1 = random.randint(1, 255)
        colour_2 = random.randint(1, 255)
        colour_3 = random.randint(1, 255)

        albedo = (colour_1 + colour_2 + colour_3) / (255 * 3)  # The rate at which planets will absorb heat.

        self.p_colour = (colour_1, colour_2, colour_3)

        # To find the expected temperature of a planet, you must set the heat radiated by a planet:
        # ( 4*PI*r^2*[STEFAN_BOLTZMANN_CONSTANT]*Temperature^4 ) equal to the heat absorbed:
        # (PI*r^2*Star_Luminosity*(1-albedo))/(4*PI*p_distance^2)
        # If we combine these and then solve for T, we get:
        #  T = ((Star_Luminosity*(1-albedo) / (16*PI*[STEFAN_BOLTZMANN_CONSTANT]))^0.25 * (1 / (p_distance**0.5))
        # absorbed
        temperature_kelvin = ((self.star_luminosity_l + (self.star_luminosity_2 * self.binary)) * ((1 - albedo) /
                              (16 * PI * STEFAN_BOLTZMANN_CONSTANT)))**0.25 / (self.p_star_distance**0.5)
        # Temperature is in Kelvin, so we must convert to degrees celcius:
        self.p_temperature = temperature_kelvin - 273

    def generate_stars(self):  # Generates the type of star/s present in the system.

        probability_binary = [0.7, 0.4]  # Reduced probability due to absence of protobinary formations
        is_star_binary = [0, 1]  # Binary = 0 if no binary system, Binary = 1 if there is a binary system.
        self.star_spectral_type.clear()  # Spectral type list for stars. 2 sets of data will be in list if binary.

        temporary_binary = random.choices(is_star_binary, weights=probability_binary, k=1)
        binary = temporary_binary[0]
        self.binary = binary

        red_dwarf = dict(type="Red Dwarf", min_mass=0.3 * SOLAR_MASS, max_mass=0.65 * SOLAR_MASS, luminosity_ratio=(0.03
                         * SOLAR_LUMINOSITY) / (0.45 * SOLAR_MASS), density=50000, colour=(244, 39, 7),
                         spectral_type="K, M")
        red_giant = dict(type="Red Giant", min_mass=0.5 * SOLAR_MASS, max_mass=10 * SOLAR_MASS, luminosity_ratio=
                         (500 * SOLAR_LUMINOSITY) / (5 * SOLAR_MASS), density=0.000175, colour=(224, 30, 0),
                         spectral_type="K, M")
        orange_dwarf = dict(type="Orange Dwarf", min_mass=0.6 * SOLAR_MASS, max_mass=0.8 * SOLAR_MASS,
                            luminosity_ratio=(0.3 * SOLAR_LUMINOSITY) / (0.7 * SOLAR_MASS), density=1600, colour=
                            (255, 110, 0), spectral_type="K")
        yellow_dwarf = dict(type="Yellow Dwarf", min_mass=0.8 * SOLAR_MASS, max_mass=1.4 * SOLAR_MASS,
                            luminosity_ratio=SOLAR_LUMINOSITY/SOLAR_MASS, density=1400, colour=(255, 243, 84),
                            spectral_type="G")
        brown_dwarf = dict(type="Brown Dwarf", min_mass=0.3 * SOLAR_MASS, max_mass=0.8 * SOLAR_MASS, luminosity_ratio=
                           (0.000001 * SOLAR_LUMINOSITY) / (0.5 * SOLAR_MASS), density=70, colour=(90, 40, 0),
                           spectral_type="M, L, T, Y")
        white_dwarf = dict(type="White Dwarf", min_mass=0.5 * SOLAR_MASS, max_mass=1.4 * SOLAR_MASS, luminosity_ratio=
                           (20 * SOLAR_LUMINOSITY) / (0.7 * SOLAR_MASS), density=10**9, colour=(255, 255, 255),
                           spectral_type="D")
        neutron_star = dict(type="Neutron Star", min_mass=1.4 * SOLAR_MASS, max_mass=3.2 * SOLAR_MASS,
                            luminosity_ratio=(0.0000001 * SOLAR_LUMINOSITY) / (2.3 * SOLAR_MASS), density=5*(10**17),
                            colour=(0, 0, 0), spectral_type="D")
        # Density is in kg/m^3

        def generate_star(n):
                                        # originally 0.004
            probability_startype = [0.6, 0.004, 0.1675, 0.1675, 0.05, 0.004,
                                    0.007]  # A realistic probability list of stars below.
            name_startype = [red_dwarf, red_giant, orange_dwarf, yellow_dwarf,  # The order of the stars in list
                             brown_dwarf, white_dwarf, neutron_star]  # correspond to probabilities above.
            temporary_name = random.choices(name_startype, weights=probability_startype, k=1)

            star_type = temporary_name[0]

            mass_range1 = star_type.get('min_mass')
            mass_range2 = star_type.get('max_mass')

            # Will generate the mass of the star, given the maximum and minimum mass range of the star type.
            star_mass = random.randint(mass_range1, mass_range2)

            # Since luminosity is directly proportional to mass, we can generate the star's luminosity by multiplying
            # mass by the luminosity ratio defined above
            star_luminosity = star_mass * star_type.get('luminosity_ratio')

            star_name = star_type.get('type')

            star_colour = star_type.get('colour')  # Will give the colour of the star

            star_volume = star_mass / star_type.get('density')
            star_radius = (3 * star_volume / (4 * PI))**(1/3)

            if n == 0:
                data.star_type_1 = star_name
                data.star_mass_1 = star_mass
                data.star_luminosity_l = star_luminosity
                orbital_visual.star_colour1 = star_colour
                data.star_radius_1 = star_radius
                data.star_spectral_type.append(star_type.get('spectral_type'))
            else:
                data.star_type_2 = star_name
                data.star_mass_2 = star_mass
                data.star_luminosity_2 = star_luminosity
                orbital_visual.star_colour2 = star_colour
                data.star_radius_2 = star_radius
                data.star_spectral_type.append(star_type.get('spectral_type'))

        for x in range(binary + 1):  # binary = 0: no binary system. Thus binary + 1 will repeat loop for stars present.
            generate_star(x)

        if binary == 1:  # Calculating the orbit distance of stars when in binary system.

            m1 = self.star_mass_1  # m1 = star mass 1

            m2 = self.star_mass_2  # m2 = 2nd star mass

            orbital_period = random.randint(12552000, 17552000)  # An average set of periods of binary stars in orbit.

        # First, we must calculate distance between stars in order to find radius of a star in the binary system.
        # We can use period formula with T = 2PI(a^3/[GRAVITY_CONSTANT](m1 + m2))^0.5 to solve for a.
            a = ((orbital_period**2)*(GRAVITY_CONSTANT*(m1 + m2))/4*PI**2)**(1/3)
        #  By combining Kepler's equation, force of gravity equation and formulae for velocity we can solve for v1 with:
            v1 = (((2*PI*GRAVITY_CONSTANT*a)/orbital_period)**(1/3))/(1 + (m1 / m2))
        # If we assume a circular orbit, we can use equation:  Pv1 = 2PI*r1, then r1 = Pv1/2PI
            r1 = orbital_period*v1/(2*PI)
        # And now we can get r2 by simply subtracting r1 from total distance.
            r2 = a - r1
            self.star_barycenter_1 = r1 * 10000000  # Distance the stars are from their barycenter.
            self.star_barycenter_2 = r2  # multiplied r1 by 10,000,000 because I forgot to convert Km to m when cubed.

            self.binary_star_distance = a  # Distance between the stars.
            self.bin_orbital_period = orbital_period


class OrbitalVisual:
    def __init__(self,):
        self.ampli_p = 0  # Amplitude of sin function that determines length of planet's orbit
        self.ampli_m = 0  # Amplitude of sin function that determines length of moon orbit
        self.scale = 0  # Scales planets, stars, and moon orbits from data down to appropriate size for window.
        self.magnified_scale = 0  # Scales moons orbits for magnified window.
        self.moon_tick_scale = []
        self.star_colour1 = (255, 255, 255)
        self.star_colour2 = (255, 255, 255)
        self.binary = 0
        self.ampli_s1 = 0  # Formulae for calculating volume with respect to radius.
        self.ampli_s2 = 0  # volume is directly proportional to mass, therefore we can use.
        self.ampli_m_m = 0
        self.bin_mod_tick = 0  # The ticker for the binary system.
        self.rand_bin_add = 0
        self.planet_x = 0   # X position of planet
        self.planet_y = 0   # Y position of planet
        self.planet_tick = 0  # Period modifier of planet
        self.planet_m_x = 0  # X pos of planet in scaled window
        self.planet_m_y = 0  # Y pos of planet in scaled window
        self.moon_x = 0    # X position of moon
        self.moon_y = 0    # Y position of moon
        self.moon_start = []  # A list of random moon starting positions, so they do not start in a line.
        self.r_m = 0  # Radii of moons in orbital visual. There is no point in having to scale size, they are too small.
        self.tick = 0

    def calculate_scale(self):
        self.rand_bin_add = random.uniform(0.0000, 4.0000)
        self.binary = (data.binary - 1) ** 2  # 0 = there is a binary star system, 1 = there is no binary star system.
        # Since data.binary works the other way around, (1 = there is no binary system, 0 = there IS a binary system,)
        # I have created an equation that will output a 1 if a 0 is input, and will output a 0 if a 1 is
        # input.

        self.bin_mod_tick = TICK_RATE / data.bin_orbital_period
        self.scale = ((SCREEN_WIDTH-200) / 4) / (data.p_star_distance + max(data.moon_orbit_distance))
        # Will calculate the appropriate scale for the orbital window
        self.magnified_scale = (((MAGNIFIED_LENGTH-30)/2) / (max(data.moon_orbit_distance)+data.p_radius*10))
        # Will calculate the appropriate scale for magnified orbital window. I added the planet radius times 10,
        # as there can be occurrences with single moon micro-orbits which result in the planet appearing much larger
        # than it should.

        self.moon_start.clear()
        self.moon_tick_scale.clear()  # Now we calculate modifier for period of orbit of moons.
        i = 0
        for _ in range(len(data.moon_colours)):

            self.moon_tick_scale.append(TICK_RATE/((2 * PI * data.moon_orbit_distance[i])/data.moon_velocity[i]))
            i += 1
# I used 2 PI to calculate distance of orbit, then divided by orbit speed to calculate
# time taken to complete orbit in seconds, then divided by TICK_RATE to obtain the scale for each moon.

            self.moon_start.append(random.randint(1, 300))  # This will determine the starting point for the moons in
            # the math.sin and math.cos functions. Since COS and SIN are periodic functions, it does not matter what
            # the random number is. This bit of code will ensure that each moon starts at a different amplitude
            # when generated so they do not all generate in a line.

        if max(data.moon_orbit_distance) > 1000000000:
            self.r_m = 1
        else:             # This bit of code makes the sizes of the moons in the magnified orbital visual.
            self.r_m = 2  # If the orbit is greater than 1,000,000 kilometers, the moons will be half the size.

    def draw_binary(self):  # Function which draws the center 2 stars, if there is a binary system present.
        x_s1 = -data.star_barycenter_1*self.scale * math.sin(self.tick*self.bin_mod_tick+self.rand_bin_add)
        y_s1 = (data.star_barycenter_1*self.scale)/2 * math.cos(self.tick*self.bin_mod_tick+self.rand_bin_add)
        x_s2 = data.star_barycenter_2*self.scale * math.sin(self.tick*self.bin_mod_tick+self.rand_bin_add)
        y_s2 = (-data.star_barycenter_2*self.scale)/2 * math.cos(self.tick*self.bin_mod_tick+self.rand_bin_add)

        arcade.draw_ellipse_outline(CENTER_X, CENTER_Y, data.star_barycenter_1 * self.scale,
                                    data.star_barycenter_1 * self.scale / 2, (60, 60, 60))
        arcade.draw_ellipse_outline(CENTER_X, CENTER_Y, data.star_barycenter_2 * self.scale,
                                    data.star_barycenter_2 * self.scale / 2, (60, 60, 60))

        arcade.draw_line(CENTER_X + x_s1, CENTER_Y + y_s1, CENTER_X + x_s2, CENTER_Y + y_s2, (100, 100, 100), 1)
        arcade.draw_circle_filled(CENTER_X + x_s1, CENTER_Y + y_s1, data.star_radius_1 * self.scale + 2,
                                  self.star_colour1)
        arcade.draw_circle_filled(CENTER_X + x_s2, CENTER_Y + y_s2, data.star_radius_2 * self.scale + 2,
                                  self.star_colour2)

    def draw_exoplanet(self, a, b, c):  # Function that draws the exoplanet.
        arcade.draw_ellipse_outline(CENTER_X, CENTER_Y, (data.p_star_distance*self.scale),
                                    ((data.p_star_distance*self.scale) // 2), (200, 200, 200), 1, 0)
        arcade.draw_line(self.planet_x, self.planet_y, CENTER_X, CENTER_Y, (0, 100, 0))
        arcade.draw_circle_filled(a, b, c, data.p_colour)
        arcade.draw_rectangle_outline(a, b, 64, 32, (255, 0, 255), 1)
        arcade.draw_line(a-32, b-16, CENTER_X_MAGNIFIED-(MAGNIFIED_LENGTH/2), CENTER_Y_MAGNIFIED+(MAGNIFIED_HEIGHT/2),
                         (255, 0, 255))
        arcade.draw_line(a+32, b-16, CENTER_X_MAGNIFIED+(MAGNIFIED_LENGTH/2), CENTER_Y_MAGNIFIED+(MAGNIFIED_HEIGHT / 2),
                         (255, 0, 255))

    def draw_exomoon(self, size, p_x, p_y, ampli, colour, i):  # Function that draws the exomoon
        x = (-self.ampli_m * math.sin(self.tick*self.moon_tick_scale[i] + self.moon_start[i]) + self.planet_x)
        y = (self.ampli_m / 2 * math.cos(self.tick*self.moon_tick_scale[i] + self.moon_start[i]) + self.planet_y)
        magnified_x = (self.ampli_m_m * math.cos(self.tick*self.moon_tick_scale[i] + self.moon_start[i]) +
                       CENTER_X_MAGNIFIED)
        magnified_y = (-self.ampli_m_m / 2 * math.sin(self.tick*self.moon_tick_scale[i] + self.moon_start[i]) +
                       CENTER_Y_MAGNIFIED)
        arcade.draw_ellipse_outline(p_x, p_y, ampli, (ampli // 2), (50, 50, 50))
        arcade.draw_circle_filled(x, y, size, colour)
        arcade.draw_circle_filled(magnified_x, magnified_y, size, colour)

    def magnified_visual(self):
        arcade.draw_rectangle_outline(CENTER_X_MAGNIFIED, CENTER_Y_MAGNIFIED, MAGNIFIED_LENGTH, MAGNIFIED_HEIGHT,
                                      (255, 0, 255))
        self.draw_exoplanet(self.planet_m_x, self.planet_m_y, data.p_radius*self.magnified_scale)

    def draw(self):
        i = 0
        for x in range(len(data.moon_colours)):
            self.ampli_m = data.moon_orbit_distance[x]*self.scale  # amplitude for orbital visual.
            self.ampli_m_m = data.moon_orbit_distance[x]*self.magnified_scale  # Scaled amplitude for sin curve in
            # magnified orbital visual.

            OrbitalVisual.draw_exomoon(self, 1, self.planet_x, self.planet_y,
                                       self.ampli_m, data.moon_colours[x], x)
            # Size has maximum 1, as it is impossible for a moon to be larger than 1 pixel in radius in regular visual.
            OrbitalVisual.draw_exomoon(self, self.r_m, CENTER_X_MAGNIFIED,
                                       CENTER_Y_MAGNIFIED, self.ampli_m_m, data.moon_colours[x], x)
            i += 1

        OrbitalVisual.draw_exoplanet(self, self.planet_x, self.planet_y, data.p_radius * self.scale + 1)
        if self.binary == 0:
            OrbitalVisual.draw_binary(self)

        arcade.draw_circle_filled(CENTER_X, CENTER_Y, (self.binary * (data.star_radius_1 * self.scale + 3)),
                                  self.star_colour1)
        arcade.draw_rectangle_outline(CENTER_X, CENTER_Y, (SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2), (255, 255, 255), 2)
        arcade.draw_rectangle_outline(CENTER_X_MAGNIFIED, CENTER_Y_MAGNIFIED, MAGNIFIED_LENGTH,
                                      MAGNIFIED_HEIGHT, (255, 0, 255), 3)
        arcade.draw_circle_filled(CENTER_X_MAGNIFIED, CENTER_Y_MAGNIFIED, (data.p_radius*self.magnified_scale)+1,
                                  data.p_colour)

    def update(self):
        self.tick += TICK/16
        self.planet_x = ((data.p_star_distance*self.scale) * math.sin(self.tick + self.moon_start[0]) + CENTER_X)
        self.planet_y = (((data.p_star_distance*self.scale) / 2) * math.cos(self.tick + self.moon_start[0]) + CENTER_Y)


class Interact:
    def __init__(self, number, interact_x, interact_y, interact_width, interact_height, interact_text, size_text):
        self.number = number
        self.interact_x = interact_x
        self.interact_y = interact_y
        self.interact_width = interact_width
        self.interact_height = interact_height
        self.interact_text = interact_text
        self.font_size = size_text

        self.colour1 = 150
        self.colour2 = 150
        self.colour3 = 150
        self.deltac = 0  # The colour change of the
        self.delta_time = 1 / 30
        self.displacement = -3

    def draw_interact(self):
        arcade.draw_rectangle_filled(self.interact_x-self.displacement, self.interact_y-self.displacement,
                                     self.interact_width, self.interact_height,
                                     (self.colour1-self.deltac-40, self.colour2-self.deltac-40,
                                      self.colour3-self.deltac-40))
        arcade.draw_rectangle_filled(self.interact_x, self.interact_y, self.interact_width, self.interact_height,
                                     (self.colour1-self.deltac, self.colour2-self.deltac, self.colour3-self.deltac))
        arcade.draw_text(self.interact_text, self.interact_x-self.interact_width//2 + 10,
                         self.interact_y-self.interact_height//3, (40-self.deltac, 40-self.deltac, 40-self.deltac),
                         font_size=self.font_size)


gen_planet = Interact(1, (SCREEN_WIDTH/4), 100, 200, 80, "Generate Planet", 14)

Interact.controls = [gen_planet]
# It was intended for there to be more than one button, so this control list is no longer used. I will still keep
# this here in case I want to add extra features to this project in the future, if I ever want to.


class Game(arcade.Window):
    def __init__(self, window, width, height, title):

        self.is_window = window
        self.pressed = 0

        self.new = 0

        super().__init__(width, height, title)
        arcade.set_background_color((0, 0, 0))

    def on_draw(self):
        arcade.start_render()
        orbital_visual.draw()
        arcade.draw_rectangle_outline(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, SCREEN_WIDTH-20, SCREEN_HEIGHT-14,
                                      (255, 255, 255), 5)
        for interact in Interact.controls:
            interact.draw_interact()
        draw_texts()

    def update(self, delta_time):
        orbital_visual.update()

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        for i in Interact.controls:
            if i.interact_x - i.interact_width/2 < x < i.interact_x + i.interact_width/2 and \
               i.interact_y - i.interact_height/2 < y < i.interact_y + i.interact_height/2:
                i.deltac = 40
                i.displacement = -4
            else:
                i.displacement = -9
                i.deltac = 0

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        for i in Interact.controls:
            if i.interact_x - i.interact_width <= x <= i.interact_x + i.interact_width and \
                    i.interact_y - i.interact_height <= y <= i.interact_y + i.interact_height:
                    i.displacement = -3
                    if i.number == 1 and self.new == 0:
                        generate_new()


#   draw_texts() DRAWS ALL THE TEXT DISPLAYED ON THE SCREEN
def draw_texts():
    reduction = 0
    star_masses = [data.star_mass_1, data.star_mass_2]
    star_types = [data.star_type_1, data.star_type_2]
    star_radius = [data.star_radius_1, data.star_radius_2]
    star_luminosities = [data.star_luminosity_l, data.star_luminosity_2]
    # Just defining some local lists so I can

    arcade.draw_text("VERY-REALISTIC PLANET GENERATOR", 40, SCREEN_HEIGHT-65, (255, 0, 110), font_size=20, bold=True)
    arcade.draw_rectangle_outline(250, SCREEN_HEIGHT-55, 450, 40, (255, 255, 255))

    for x in range(len(data.p_surface_materials)):
        arcade.draw_text("{}".format(data.p_surface_materials[x]), 20, (SCREEN_HEIGHT - 130 - reduction),
                         (255, 255, 255))
        try :
            arcade.draw_text("{}".format(data.p_surface_materials_named[x]), 160, (SCREEN_HEIGHT - 130 - reduction),
                             (255, 255, 255))
        except: continue          # If index out of range, we can skip so that for loop can continue.
        reduction += 20

    arcade.draw_text("Earth masses:     {}".format(round(data.p_mass/EARTH_MASS, 2)), 20, SCREEN_HEIGHT - 230,
                     (0, 100, 255))
    arcade.draw_text("Planet Radius:   {} Km".format(round(data.p_radius/1000, 2)), 20, SCREEN_HEIGHT - 260,
                     (0, 100, 255))
    arcade.draw_text("Moons:   {}".format(len(data.moon_orbit_distance)), 20, SCREEN_HEIGHT - 290, (0, 100, 255))
    arcade.draw_text('Most Common Surface Matter:', 20, SCREEN_HEIGHT-110, (255, 0, 100))
    arcade.draw_text('Gravitational Acceleration:   -{} ms^-2'.format(round(data.p_gravity_strength, 2)), 20, SCREEN_HEIGHT -
                     320, (0, 100, 255))
    arcade.draw_text('Estimated Atmosphere Pressure:  {}  Pascals'.format(round(data.p_atmosphere_pressure, 2)), 20,
                     SCREEN_HEIGHT - 350, (0, 100, 255))
    arcade.draw_text('Planet Temperature:  {} Degrees Celcius'.format(round(data.p_temperature, 2)), 20, SCREEN_HEIGHT
                     - 380, (0, 140, 255))
    arcade.draw_text('[Greenhouse effect was not included in calculation, as exact \n atmosphere conditions are '
                     'unknown. Expect surface \n temperature to be lower than what it actually would be.]', 20,
                     SCREEN_HEIGHT - 400, (0, 140, 255))
    reduction = 0
    arcade.draw_text('Prominent Gas/es:', 20, SCREEN_HEIGHT - 470 - reduction,
                     (255, 255, 255))
    arcade.draw_text('Distance from star: {} Astronomical Units'.format(round(data.p_star_distance / ASTRONOMICAL_UNIT,
                                                                              3)), 20, SCREEN_HEIGHT - 550,
                     (0, 100, 255))
    for x in range(len(data.p_atmosphere_type)):
        arcade.draw_text('Gas {}: {}'.format(x+1, data.p_atmosphere_type[x]), 20, SCREEN_HEIGHT - 490 - reduction,
                         (255, 255, 255))
        reduction += 20
    arcade.draw_text("Orbital Visual - 6 Months per second", SCREEN_WIDTH / 4 * 3 - 130, SCREEN_HEIGHT - 40,
                     (255, 255, 255), bold=True)
    arcade.draw_text("Moon Visual - 6 Months per second", SCREEN_WIDTH / 4 * 3 - 150, SCREEN_HEIGHT / 2 - 82,
                     (255, 0, 255), bold=True)
    arcade.draw_text("Exoplanet is in center of window", SCREEN_WIDTH / 4 * 3 - 150, SCREEN_HEIGHT / 2 - 110,
                     (255, 0, 255))
    reduction = 0
    for x in range(data.binary+1):
        arcade.draw_text('Star {}:  {}'.format(x+1, star_types[x]), SCREEN_WIDTH/2-290, SCREEN_HEIGHT - 110 - reduction,
                         (255, 0, 100))
        arcade.draw_text('Spectral Type:  {}'.format(data.star_spectral_type[x]), SCREEN_WIDTH / 2 - 290, SCREEN_HEIGHT -
                         130 - reduction, (255, 255, 255))
        arcade.draw_text('Solar Mass:  {}'.format(round(star_masses[x]/SOLAR_MASS, 6)), SCREEN_WIDTH/2 - 290,
                         SCREEN_HEIGHT - 150 - reduction, (255, 255, 255))
        arcade.draw_text('Star Radius (Km):  {}'.format(round(star_radius[x]/1000, 2)), SCREEN_WIDTH / 2 - 290,
                         SCREEN_HEIGHT - 170 - reduction, (255, 255, 255))
        arcade.draw_text('Star Luminosity (L):  {}'.format(round(star_luminosities[x]/SOLAR_LUMINOSITY, 7)), SCREEN_WIDTH /
                         2 - 290, SCREEN_HEIGHT - 190 - reduction, (255, 255, 255))
        reduction += 115
    arcade.draw_text("Orbitals will appear slightly bigger in orbital window than they will in real life.",
                     SCREEN_WIDTH/2 + 60, SCREEN_HEIGHT - 80, (70, 70, 70), font_size=12)


data = Data()
orbital_visual = OrbitalVisual()


# The function called when generating a whole new planet a set of stars.
def generate_new():
    data.generate_stars()
    data.general_generation()
    data.moon_generate()
    orbital_visual.calculate_scale()
    orbital_visual.tick = 0
    data.planet_resource_generate()
    data.other_material_generate()
    draw_texts()


# Main
def main():
    Game(1, SCREEN_WIDTH, SCREEN_HEIGHT, "RANDOM PLANET GEN")
    generate_new()
    arcade.run()


main()


