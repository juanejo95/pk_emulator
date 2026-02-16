from dash import Dash, html, dcc, Input, Output
import plotly.graph_objects as go
import numpy as np

from predict_pk import predict_pk

# print(a)

app = Dash(__name__)

# Load parameter bounds
param_bounds = np.load("results/param_bounds.npz")
h_bounds = param_bounds["h_bounds"]
Omega_c_bounds = param_bounds["Omega_c_bounds"]
Omega_b_bounds = param_bounds["Omega_b_bounds"]
Asx1e9_bounds = param_bounds["Asx1e9_bounds"]
ns_bounds = param_bounds["ns_bounds"]
mnu_bounds = param_bounds["mnu_bounds"]

# Default cosmology
h_default = 0.67
Omega_c_default = 0.25
Omega_b_default = 0.045
Asx1e9_default = 2.1
ns_default = 0.97
mnu_default = 0.06

# Load the kh vector
kh = np.load("results/k_grid.npy")

pk_default = predict_pk([h_default, Omega_c_default, Omega_b_default, Asx1e9_default, ns_default, mnu_default])

app.layout = html.Div([

    html.H2(
        "Matter Power Spectrum Emulator",
        style={
            'textAlign': 'center',
            'fontFamily': '"Times New Roman", serif',
            'fontSize': '36px',
            'color': '#1f77b4',
            'textShadow': '2px 2px 4px rgba(0,0,0,0.3)',
            'marginTop': '20px',
            'marginBottom': '20px',
            'fontWeight': 'bold',
        }
    ),
    
    html.Div([
        # Left: Graph
        html.Div([
            dcc.Graph(
                id="pk-plot",
                mathjax=True,
                style={'width': '100%', 'height': '100%'},
                config={'responsive': True}
            )
        ], style={
            'flex': '2',
            'padding': '10px',
            'display': 'flex',
            'flexDirection': 'column',
            'font-size': '30px'  # fontsize for x and y axis
        }),

        # Right: Sliders
        html.Div([
            dcc.Markdown(r"$h$", mathjax=True, style={'font-size': '20px'}),
            dcc.Slider(
                min=h_bounds[0],
                max=h_bounds[1],
                step=(h_bounds[1]-h_bounds[0])/50,
                value=h_default,
                marks={
                    h_bounds[0]: f"{h_bounds[0]:.2f}",
                    h_bounds[1]: f"{h_bounds[1]:.2f}"
                },
                id="h",
                updatemode='drag',
            ),
            html.Br(),

            dcc.Markdown(r"$\Omega_{\rm c}$", mathjax=True, style={'font-size': '20px'}),
            dcc.Slider(
                min=Omega_c_bounds[0],
                max=Omega_c_bounds[1],
                step=(Omega_c_bounds[1]-Omega_c_bounds[0])/50,
                value=Omega_c_default,
                marks={
                    Omega_c_bounds[0]: f"{Omega_c_bounds[0]:.2f}",
                    Omega_c_bounds[1]: f"{Omega_c_bounds[1]:.2f}"
                },
                id="Omega_c",
                updatemode='drag',
            ),
            html.Br(),

            dcc.Markdown(r"$\Omega_{\rm b}$", mathjax=True, style={'font-size': '20px'}),
            dcc.Slider(
                min=Omega_b_bounds[0],
                max=Omega_b_bounds[1],
                step=(Omega_b_bounds[1]-Omega_b_bounds[0])/50,
                value=Omega_b_default,
                marks={
                    Omega_b_bounds[0]: f"{Omega_b_bounds[0]:.2f}",
                    Omega_b_bounds[1]: f"{Omega_b_bounds[1]:.2f}"
                },
                id="Omega_b",
                updatemode='drag',
            ),
            html.Br(),

            dcc.Markdown(r"$A_{\rm s}\cdot 10^9$", mathjax=True, style={'font-size': '20px'}),
            dcc.Slider(
                min=Asx1e9_bounds[0],
                max=Asx1e9_bounds[1],
                step=(Asx1e9_bounds[1]-Asx1e9_bounds[0])/50,
                value=Asx1e9_default,
                marks={
                    Asx1e9_bounds[0]: f"{Asx1e9_bounds[0]:.2f}",
                    Asx1e9_bounds[1]: f"{Asx1e9_bounds[1]:.2f}"
                },
                id="Asx1e9",
                updatemode='drag',
            ),
            html.Br(),

            dcc.Markdown(r"$n_{\rm s}$", mathjax=True, style={'font-size': '20px'}),
            dcc.Slider(
                min=ns_bounds[0],
                max=ns_bounds[1],
                step=(ns_bounds[1]-ns_bounds[0])/50,
                value=ns_default,
                marks={
                    ns_bounds[0]: f"{ns_bounds[0]:.2f}",
                    ns_bounds[1]: f"{ns_bounds[1]:.2f}"
                },
                id="ns",
                updatemode='drag',
            ),
            html.Br(),

            dcc.Markdown(r"$\sum_\nu m_\nu$", mathjax=True, style={'font-size': '20px'}),
            dcc.Slider(
                min=mnu_bounds[0],
                max=mnu_bounds[1],
                step=(mnu_bounds[1]-mnu_bounds[0])/50,
                value=mnu_default,
                marks={
                    mnu_bounds[0]: f"{mnu_bounds[0]:.2f}",
                    mnu_bounds[1]: f"{mnu_bounds[1]:.2f}"
                },
                id="mnu",
                updatemode='drag',
            ),
            html.Br(),

            html.Button(
                "Reset to default cosmology",
                id="reset-button",
                n_clicks=0,
                style={
                    "backgroundColor": "#1f77b4",  # same as above
                    "color": "white",
                    "border": "none",
                    "padding": "10px 20px",
                    "textAlign": "center",
                    "textDecoration": "none",
                    "display": "inline-block",
                    "fontSize": "16px",
                    "marginTop": "10px",
                    "borderRadius": "8px",
                    "cursor": "pointer",
                    "transition": "background-color 0.3s"
                }
            )
        ], style={'flex': '1', 'padding': '10px', 'display': 'flex', 'flexDirection': 'column'})
    ], style={'display': 'flex', 'flex': '1', 'height': '80vh'})  # <-- take 80% of viewport height
], style={'display': 'flex', 'flexDirection': 'column', 'height': '100vh'})

# Callback: Update figure when sliders change
@app.callback(
    Output("pk-plot", "figure"),
    Input("h", "value"),
    Input("Omega_c", "value"),
    Input("Omega_b", "value"),
    Input("Asx1e9", "value"),
    Input("ns", "value"),
    Input("mnu", "value"),
)
def update_pk(h, Omega_c, Omega_b, Asx1e9, ns, mnu):
    pk = predict_pk([h, Omega_c, Omega_b, Asx1e9, ns, mnu])

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=kh, y=pk_default*h_default**3, mode="lines", line=dict(color="black")))
    fig.add_trace(go.Scatter(x=kh, y=pk*h**3, mode="lines"))

    y_min = 1e-1  # adjust if needed
    y_max = 5e4   # adjust if needed

    fig.update_layout(
        showlegend=False,
        xaxis=dict(
            type="log",
            exponentformat="e",
            showexponent="all",
            title=r"$k\ [h/{\rm Mpc}]$",
        ),
        yaxis=dict(
            type="log",
            exponentformat="e",
            showexponent="all",
            title=r"$P(k)\ [{\rm Mpc}^3]$",
            range=[np.log10(y_min), np.log10(y_max)]
        ),
        font=dict(
            family="Computer Modern, serif",
            size=20
        )
    )
    return fig

# Callback: Reset sliders to default cosmology
@app.callback(
    Output("h", "value"),
    Output("Omega_c", "value"),
    Output("Omega_b", "value"),
    Output("Asx1e9", "value"),
    Output("ns", "value"),
    Output("mnu", "value"),
    Input("reset-button", "n_clicks")
)
def reset_sliders(n_clicks):
    return h_default, Omega_c_default, Omega_b_default, Asx1e9_default, ns_default, mnu_default

if __name__ == "__main__":
    app.run(debug=True)
