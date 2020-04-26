import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

topmetrics = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Card([dbc.CardBody(
                                            [
                                                html.H5(
                                                    id="confirm_cases_card",
                                                    className="card-title",
                                                ),
                                                html.P("Confirmed Cases (prev day)", className="card-text"),
                                            ]
                                        )],
                                        )
                                    ]
                                ),
                                dbc.Col(
                                    [
                                        dbc.Card([dbc.CardBody(
                                            [
                                                html.H5(
                                                    id="death_cases_card",
                                                    className="card-title",
                                                ),
                                                html.P("Deaths (prev day)", className="card-text"),
                                            ]
                                        )],
                                        )
                                    ]
                                ),
                                dbc.Col(
                                    [
                                        dbc.Card([dbc.CardBody(
                                            [
                                                html.H5(
                                                    id="mortality_card",
                                                    className="card-title",
                                                ),
                                                html.P("Mortality Rate", className="card-text"),
                                            ]
                                        )],
                                        )
                                    ]
                                ),
                            ]
                        )
                    ], className =['col-7', 'ml-0' , 'mr-0', 'mt-0' , 'mb-0']
                ),
                dbc.Col(
                    [                        
                        dbc.Row(
                            [
                                dbc.Col(
                                    [                        
                                        dbc.Card([dbc.CardBody(
                                            [
                                                html.H5(
                                                    id="growth_confirm_card",
                                                    className="card-title",
                                                ),
                                                html.P("Growth Confirmed Cases (%)", className="card-text"),
                                            ]
                                        ),],
                                        )
                                    ]
                                ),                                    
                                dbc.Col(
                                    [dbc.Card([dbc.CardBody(
                                            [
                                                html.H5(
                                                    id="growth_death_card",
                                                    className="card-title",
                                                ),
                                                html.P("Growth Deaths (%)", className="card-text"),
                                            ]
                                        ),
                                        ],                                        
                                    )]
                                )
                            ]
                        )
                    ], className =['col-5', 'ml-0' , 'mr-0', 'mt-0' , 'mb-0']
                )
            ], className= ['justify-content-between', 'ml-2' , 'mr-2', 'mt-2' , 'mb-2'],
        )
    ]
)