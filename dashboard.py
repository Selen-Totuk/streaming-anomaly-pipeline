import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import numpy as np
import webbrowser
from threading import Timer

# Veriyi yükle
df = pd.read_csv("data/processed/comparison_results.csv")
df['date'] = pd.to_datetime(df['date'])
df['total_listening_hours'] = df['total_listening_sec'] / 3600

# Renk paleti
colors = {
    'both': '#FF4B4B',
    'ml_only': '#4B8BFF',
    'rule_only': '#FFD94B',
    'none': '#9CA3AF'
}

# Dash uygulaması
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    # Başlık
    dbc.Row([
        dbc.Col(html.H1("🎵 Anomali Detection Dashboard", 
                       className="text-center my-4 text-success"), width=12)
    ]),
    
    # Özet kartları
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("Toplam Kayıt", className="card-title"),
                html.H2(f"{len(df):,}", className="text-primary")
            ])
        ]), width=3),
        
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("Toplam Anomali", className="card-title"),
                html.H2(f"{(df['decision_group'] != 'none').sum():,}", 
                       className="text-danger")
            ])
        ]), width=3),
        
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("Ortalama Dinleme", className="card-title"),
                html.H2(f"{df['total_listening_hours'].mean():.1f} saat", 
                       className="text-success")
            ])
        ]), width=3),
        
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("Anomali Oranı", className="card-title"),
                html.H2(f"{(df['decision_group'] != 'none').mean()*100:.1f}%", 
                       className="text-warning")
            ])
        ]), width=3),
    ], className="mb-4"),
    
    # Filtreler
    dbc.Row([
        dbc.Col([
            html.Label("📊 Anomali Grubu:"),
            dcc.Dropdown(
                id='group-filter',
                options=[{'label': 'Tümü', 'value': 'all'}] +
                        [{'label': g, 'value': g} for g in df['decision_group'].unique()],
                value='all'
            ),
        ], width=4),
        
        dbc.Col([
            html.Label("👤 Kullanıcı:"),
            dcc.Dropdown(
                id='user-filter',
                options=[{'label': f'Kullanıcı {i}', 'value': i} 
                        for i in sorted(df['user_id'].unique())[:20]],
                placeholder="Kullanıcı seçin..."
            ),
        ], width=4),
        
        dbc.Col([
            html.Label("📅 Tarih:"),
            dcc.DatePickerRange(
                id='date-filter',
                start_date=df['date'].min(),
                end_date=df['date'].max(),
                display_format='YYYY-MM-DD'
            ),
        ], width=4),
    ], className="mb-4"),
    
    # Grafikler - 1. Satır
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("📈 Dağılım Grafiği (Dinleme Süresi vs Gece Oranı)"),
            dbc.CardBody(dcc.Graph(id='scatter-plot'))
        ]), width=8),
        
        dbc.Col(dbc.Card([
            dbc.CardHeader("🥧 Grup Dağılımı"),
            dbc.CardBody(dcc.Graph(id='pie-chart'))
        ]), width=4),
    ], className="mb-4"),
    
    # Grafikler - 2. Satır
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("📊 Feature Dağılımları"),
            dbc.CardBody(dcc.Graph(id='box-plots'))
        ]), width=6),
        
        dbc.Col(dbc.Card([
            dbc.CardHeader("📉 Zaman Serisi"),
            dbc.CardBody(dcc.Graph(id='time-series'))
        ]), width=6),
    ], className="mb-4"),
    
    # Veri tablosu
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("📋 Anomali Listesi"),
            dbc.CardBody([
                html.Div(id='data-table')
            ])
        ]), width=12),
    ]),
    
], fluid=True)

# Callback'ler
@app.callback(
    [Output('scatter-plot', 'figure'),
     Output('pie-chart', 'figure'),
     Output('box-plots', 'figure'),
     Output('time-series', 'figure'),
     Output('data-table', 'children')],
    [Input('group-filter', 'value'),
     Input('user-filter', 'value'),
     Input('date-filter', 'start_date'),
     Input('date-filter', 'end_date')]
)
def update_graphs(group, user, start_date, end_date):
    # Veriyi filtrele
    filtered_df = df.copy()
    
    if group and group != 'all':
        filtered_df = filtered_df[filtered_df['decision_group'] == group]
    
    if user:
        filtered_df = filtered_df[filtered_df['user_id'] == user]
    
    if start_date:
        filtered_df = filtered_df[filtered_df['date'] >= start_date]
    if end_date:
        filtered_df = filtered_df[filtered_df['date'] <= end_date]
    
    # 1. Scatter plot
    scatter_fig = px.scatter(
        filtered_df,
        x='total_listening_hours',
        y='night_ratio',
        color='decision_group',
        color_discrete_map=colors,
        hover_data=['user_id', 'date', 'track_count'],
        title=f'Toplam {len(filtered_df)} kayıt'
    )
    scatter_fig.update_layout(transition_duration=500)
    
    # 2. Pie chart
    group_counts = filtered_df['decision_group'].value_counts()
    pie_fig = px.pie(
        values=group_counts.values,
        names=group_counts.index,
        color=group_counts.index,
        color_discrete_map=colors,
        title='Grup Dağılımı'
    )
    
    # 3. Box plots
    box_fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=['Dinleme Süresi (saat)', 'Gece Oranı', 'Track Sayısı']
    )
    
    for idx, (col, title) in enumerate([
        ('total_listening_hours', 'Dinleme'),
        ('night_ratio', 'Gece'),
        ('track_count', 'Track')
    ], 1):
        for group_name in filtered_df['decision_group'].unique():
            group_data = filtered_df[filtered_df['decision_group'] == group_name]
            box_fig.add_trace(
                go.Box(
                    y=group_data[col],
                    name=group_name,
                    legendgroup=group_name,
                    showlegend=(idx==1),
                    marker_color=colors.get(group_name, '#000000')
                ),
                row=1, col=idx
            )
    
    box_fig.update_layout(height=400)
    
    # 4. Time series
    daily_counts = filtered_df.groupby(
        [filtered_df['date'].dt.date, 'decision_group']
    ).size().unstack(fill_value=0)
    
    time_fig = go.Figure()
    for group_name in daily_counts.columns:
        time_fig.add_trace(go.Scatter(
            x=daily_counts.index,
            y=daily_counts[group_name],
            name=group_name,
            mode='lines+markers',
            line=dict(color=colors.get(group_name, '#000000'), width=2)
        ))
    time_fig.update_layout(
        title='Günlük Anomali Sayıları',
        xaxis_title='Tarih',
        yaxis_title='Sayı',
        height=400
    )
    
    # 5. Data table
    table = dbc.Table.from_dataframe(
        filtered_df[['user_id', 'date', 'total_listening_hours', 'night_ratio', 
                    'track_count', 'decision_group']].head(20).round(2),
        striped=True,
        bordered=True,
        hover=True,
        size='sm'
    )
    
    return scatter_fig, pie_fig, box_fig, time_fig, table

# Tarayıcıyı otomatik aç
def open_browser():
    webbrowser.open_new("http://127.0.0.1:8050/")

if __name__ == '__main__':
    Timer(1, open_browser).start()
    # DÜZELTME: run_server yerine run kullan
    app.run(debug=True, port=8050)