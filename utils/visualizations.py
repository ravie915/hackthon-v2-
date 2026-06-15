import plotly.graph_objects as go
import plotly.express as px

def create_eligibility_gauge(match_percentage):
    """Create animated eligibility gauge."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=match_percentage,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Eligibility Match"},
        delta={'reference': 50},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 25], 'color': "lightgray"},
                {'range': [25, 50], 'color': "gray"},
                {'range': [50, 75], 'color': "lightgreen"},
                {'range': [75, 100], 'color': "green"},
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    return fig

def create_timeline(events):
    """Create application timeline."""
    fig = go.Figure()
    
    for event in events:
        fig.add_trace(go.Scatter(
            x=[event['date']],
            y=[event['stage']],
            mode='markers+text',
            text=event['title'],
            textposition="top center",
            marker=dict(size=15, color='#1a3c5e')
        ))
    
    fig.update_layout(
        height=400,
        showlegend=False,
        hovermode='closest'
    )
    return fig

def create_heatmap(data):
    """Create program eligibility heatmap."""
    fig = go.Figure(data=go.Heatmap(
        z=data['z'],
        x=data['x'],
        y=data['y'],
        colorscale='RdYlGn'
    ))
    fig.update_layout(height=400)
    return fig