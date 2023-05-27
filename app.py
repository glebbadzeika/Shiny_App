from ipyleaflet import Marker, MarkerCluster, Popup, DivIcon, CircleMarker, AntPath
from ipywidgets import HTML
from shiny import ui, render, App, reactive
from shinywidgets import register_widget, output_widget
from matplotlib import pyplot as plt
import pandas as pd
import ipyleaflet as ipyl

# df = pd.read_csv('data/arrdelay_age_1996_2007.csv')
engines_aircrafts = pd.read_csv('data/engines_and_aircrafts.csv')
airports = pd.read_csv('data/airports_to.csv')
companies = pd.read_csv('data/carriers_mean_dist.csv')
carriers_routes = pd.read_csv('data/carriers_routes.csv')

choices = ['737-3TO', '747-451', '757-224', '767-332', 'DC-9-31', '737-524', '737-3G7', '737-33A', '747-422', '150',
           '421C',
           '737-322', 'DC-9-82(MD-82)', '767-2B7', 'A320-211', '737-3S3', '767-223', 'DC-9-32', 'A320-212', '767-323',
           '690A',
           'PA-32RT-300', '172E', 'DC-7BF', 'E-90', 'DC-9-51', 'A320-232', 'S55A', '737-401', 'PA-28-180', '737-4B7',
           'DC-9-83(MD-83)',
           '182P', '172M', '757-222', '757-251', '737-3B7', '206B', 'T210N', '550', '60', 'PA-31-350', 'C90',
           'PA-32R-300', 'FALCON XP',
           'HST-550', 'KITFOX IV', 'OTTER DHC-3', '737-301', '210-5(205)', '757-232', '757-223', 'F85P-1', '65-A90',
           'A320-231', '767-322',
           '757-212', 'DC-9-41', '737-4Q8', '737-490', '777-222', '737-4S3', 'MD-88', '757-2S7', 'MD-90-30', '737-522',
           '757-2G7', '757-225',
           '767-3P6', '757-2Q8', 'MD 83', '737-3Y0', '767-324', 'FALCON-XP', '757-231', 'A319-131', '757-26D',
           'A320-214', '737-824', '737-724',
           '737-832', 'DA 20-A1', 'A319-112', '777-224', 'A319-132', 'A319-114', '737-790', '737-73A', '737-2Y5',
           '737-230', '737-282', '737-282C', '777-232',
           'CL-600-2B19', '767-424ER', '767-224', 'A321-211', '737-990', '737-924', 'A109E', '757-324', '767-432ER',
           'EMB-145LR', 'EMB-145XR', 'EMB-135LR', 'EMB-145EP', 'EMB-135ER',
           'EMB-120ER', 'EMB-120', 'EMB-145', 'S-76A', 'G-IV', '182A', '717-200', '767-33A', '757-351', '767-3CB',
           'ATR-72-212', 'CL-600-2C10', '737-3H4', '737-3L9', '737-317', '737-3Q8',
           '737-3T5', '737-3A4', '737-7H4', '747-2B5F', 'EMB-135KL', '737-76N', '737-7BD', '757-33N', 'A318-111',
           'A319-111', 'ERJ 190-100 IGW', '757-2B7', '757-23N', '767-201', 'A330-323',
           'DHC-8-202', '737-890', '737-8FH', '737-7Q8', '737-236', '737-2P6', 'CL600-2D24', 'SAAB 340B', '737-705',
           'T337G', '737-3K2', '737-5H4', '737-76Q', '737-7AD', '737-2X6C', 'A330-223']

companies_list = companies['Description'].unique().tolist()

aircraft_types = ['Fixed Wing Multi-Engine', 'Fixed Wing Single-Engine', 'Rotorcraft']
engine_types = ['Turbo-Fan', 'Turbo-Jet', 'Reciprocating', 'Turbo-Prop', 'Turbo-Shaft', '4 Cycle']
long = airports['long'].tolist()
lat = airports['lat'].tolist()
nam = airports['iata'].tolist()
time = airports['TaxiOut'].tolist()

lat2 = []
long2 = []
df3 = []

lat3 = []
long3 = []
lat3_1 = []
long3_1 = []
delay = []

app_ui = ui.page_fluid(
    ui.h2("The Reliability of the Aircraft Industry"),
    ui.HTML(
        "<p>The data presented in the plot suggests a zero correlation between the age of an aircraft and the frequency"
        " of air delays. This may appear counterintuitive to some, as one might expect older aircraft to be more prone to "
        "technical issues that could lead to delays. However, this phenomenon can largely be attributed to the extreme "
        "reliability of the aircraft industry.</p><h3>Contributing Factors:</h3><ul><li><b>Strict Maintenance Schedules</b>: "
        "Airlines follow rigorous maintenance protocols to ensure the safety and efficiency of their aircraft. These protocols"
        " are defined by regulatory authorities and are independent of the age of the aircraft. This means that an older plane will"
        " receive the same, if not more, attention compared to a newer one, ensuring that all aircraft are in optimal condition.</li>"
        "<li><b>High Quality of Manufacturing</b>: Aircraft are built to last. The manufacturers, such as Boeing and Airbus, employ high-precision "
        "engineering and robust quality control processes to ensure the longevity and durability of their planes. This results in aircraft that can reliably "
        "serve for decades.</li><li><b>Continuous Upgrades and Overhauls</b>: Even though an aircraft may be old, it doesn't mean it's outdated. Aircraft often undergo"
        " system upgrades and overhauls, including replacements of engines and other critical parts, throughout their service life. This means that an old plane might have"
        " newer parts than a relatively new plane.</li><li><b>Redundancy Systems</b>: Aircraft are designed with numerous backup systems to ensure safety and reliability. In the event "
        "of a system failure, these redundancies can take over, reducing the likelihood of delays.</li><li><b>Highly Trained Personnel</b>: Pilots, engineers, and maintenance crews are "
        "extensively trained to handle a wide range of potential issues. This high level of expertise contributes to the overall reliability of aircraft operations, regardless of the age of"
        " the plane.</li></ul><p>In conclusion, while the age of an aircraft could theoretically impact its reliability, the rigorous standards of the aircraft industry effectively mitigate this. "
        "The result is a near-zero correlation between aircraft age and air delays, as demonstrated in the plot.</p>"),

    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_selectize(
                "x", label="Model",
                choices=choices,  multiple=True,selected=choices[0]
            ),
            ui.input_selectize(
                "y", label="Year",
                choices=[i for i in range(1996, 2008)], multiple=False
            )),
        ui.panel_main(ui.output_plot("a_scatter_plot"))),

    ui.h2('Interactive Map of U.S. Airports'),

    output_widget("map"),
    ui.HTML(
        '<h2>Aircraft Performance Analysis</h2><p>This scatter plot visualizes the relationship between the time a plane '
        'spends in the air (in minutes) and the distance it travels (in miles), grouped by aircraft and engine types. It '
        'offers a compelling comparison of performance characteristics across different categories of aircraft and engines.'
        '</p><p>There is a positive correlation between time and distance for all types of aircraft and engines - the longer'
        ' a plane is in the air, the farther it travels. However, the strength of this correlation varies depending on the '
        'aircraft and engine type.</p><p>\'Fixed Wing Multi-Engine\' aircraft, particularly those with \'Turbo-Fan\' or'
        ' \'Turbo-Jet\' engines, show a strong positive correlation. These commercial or cargo planes are designed for '
        'long-haul flights and cover more distance the longer they are in the air.</p><p>\'Rotorcraft\' with \'Turbo-Shaft\''
        ' engines show a weaker correlation. Helicopters, despite spending considerable time in the air, cover shorter distances'
        ' due to their lower speed.</p><p>\'Fixed Wing Single-Engine\' aircraft, especially those with \'Reciprocating\' or '
        '\'4 Cycle\' engines, exhibit a moderate correlation. These smaller private or training aircraft don\'t usually '
        'undertake very long flights, resulting in a less pronounced time-distance relationship.</p><p>This interpretation reveals a clear'
        ' relationship between the type of aircraft and engine, and the correlation between flight time and distance traveled.'
        ' It underscores the diversity in performance characteristics across different types of aircraft and engines.</p>'),
    ui.layout_sidebar(
        ui.panel_main(ui.output_plot("ea_types_plot")),
        ui.panel_sidebar(
            ui.input_selectize(
                "x1", label="Engine type",
                choices=engine_types, multiple=True,selected=engine_types[0]
            ),
            ui.input_selectize(
                "y1", label="Aircraft type",
                choices=aircraft_types, multiple=True,selected=aircraft_types[0]
            )),
    ),
    ui.h2('Interactive Map of U.S. Airports'),
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_selectize(
                "x2", label="Company name",
                choices=companies_list, multiple=False
            ),
        ui.HTML('<h2>Map 1: Air Company\'s Radius Coverage from Different Airports (Comparison)</h2>'
                '<p>This map compares the coverage areas of an air company from different airports using'
                ' radiuses, allowing for easy visual comparison.</p>'
                '<h2>Map 2: Top 30 Most Popular Routes of '
                'the Air Company</h2><p>This map displays the air company\'s top 30 most popular routes, helping passengers identify key connections and popular destinations.</p>')),
        ui.panel_main(output_widget("map2"),output_widget("map3"),
                      )
    ),



)


def server(input, output, session):
    # companies[companies['CompanyName'].isin(input.x2())]['lat'].tolist()
    # long2 = companies[companies['CompanyName'].isin(input.x2())]['long'].tolist()
    map = ipyl.Map(zoom=4, center=(lat[0], long[0]), close_popup_on_click=False)
    for i in range(len(lat)):
        marker = Marker(location=(lat[i], long[i]), draggable=False,
                        title=str(nam[i]) + ' MeanTaxiOut: ' + str(time[i]))

        map.add(marker)

    register_widget("map", map)

    @output
    @render.plot()
    def map():

        map2 = ipyl.Map(zoom=4, center=(lat[0], long[0]), close_popup_on_click=False)
        lat2 = companies[companies['Description'] == input.x2()]['lat'].tolist()
        long2 = companies[companies['Description'] == input.x2()]['long'].tolist()
        size = companies[companies['Description'] == input.x2()]['Distance'].tolist()
        for i in range(len(lat2)):
            circle_marker = CircleMarker()
            circle_marker.location = (lat2[i], long2[i])
            circle_marker.radius = int(size[i] / 100)
            circle_marker.color = "#7590ba"
            circle_marker.fill_color = "#7590ba"
            map2.add(circle_marker)

        register_widget("map2", map2)


    @reactive.Effect
    @reactive.event(input.x2)
    def map3():


        df33 = carriers_routes[carriers_routes['Description'] == input.x2()]
        df33 = df33.sort_values('count', ascending=False)
        df33 = df33.head(30)
        lat33 = df33['lat1'].tolist()
        long33 = df33['long1'].tolist()
        lat33_1 = df33['lat2'].tolist()
        long33_1 = df33['long2'].tolist()
        delay33 = df33['count'].tolist()
        map33 = ipyl.Map(zoom=4, center=(lat33[0], long33[0]), close_popup_on_click=False)

        for i33 in range(len(lat33)):
            ant_path = AntPath(
                locations=[
                    [lat33[i33], long33[i33]], [lat33_1[i33], long33_1[i33]],
                ],
                dash_array=[1, 2, int(1000/delay33[i33])],
                delay=delay33[i33],
                color='#7590ba',
                pulse_color='#3f6fba'
            )
            marker1 = Marker(location=(lat33[i33], long33[i33]), draggable=False)
            marker2 = Marker(location=(lat33_1[i33], long33_1[i33]), draggable=False)

            map33.add(ant_path)
            map33.add(marker1)
            map33.add(marker2)

        register_widget("map3", map33)

    # print(companies['lat'].tolist())

    @output
    @render.plot
    def a_scatter_plot():
        df = pd.read_csv('data/flights_age_arrdelay/' + str(input.y()) + '.csv')
        df_1 = df[df['model'].isin(input.x())]

        plt.xlabel('Age (in years)')
        plt.ylabel('Airdelays (in mins)')

        return plt.scatter(df_1['age'], df_1['delay_sum'], s=1)

    @output
    @render.table
    def airports():
        return airports

    @output
    @render.plot
    def ea_types_plot():
        # df_1=engines_aircrafts[(engines_aircrafts['engine_type'].isin(input.x1())) &
        #                        (engines_aircrafts['aircraft_type'].isin(input.y1()))]

        fig, ax = plt.subplots()
        for e in input.x1():
            for a in input.y1():
                df_1 = engines_aircrafts[(engines_aircrafts['engine_type'] == str(e)) &
                                         (engines_aircrafts['aircraft_type'] == str(a))]
                ax.scatter(df_1['CRSElapsedTime'], df_1['Distance'], s=10, label=str(e) + '/' + str(a))

        plt.xlabel('Time (in minutes)')
        plt.ylabel('Distance (in miles)')
        plt.legend(loc="upper left")

        return fig


app = App(app_ui, server)
