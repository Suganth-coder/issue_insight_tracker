<script>
    import { onMount, onDestroy } from 'svelte';
    import Chart from 'chart.js/auto';
    
    export let issues = [];
    export let showModal = false;
    
    let chartInstance = null;
    
    $: if (showModal && issues) {
        setTimeout(renderChart, 100);
    }
    
    function closeModal() {
        showModal = false;
    }
    
    function renderChart() {
        const ctx = document.getElementById('severityChart');
        if (!ctx) return;
        
        if (chartInstance) {
            chartInstance.destroy();
        }
        
        // Filtering based on openIssues
        const openIssues = issues.filter(issue => issue.status === 'open');
        
        const severityCounts = {
            'low': 0,
            'medium': 0,
            'high': 0,
            'critical': 0
        };
        
        openIssues.forEach(issue => {
            const severity = issue.severity || 'low';
            if (severity in severityCounts) {
                severityCounts[severity]++;
            }
        });
        
        const labels = Object.keys(severityCounts).map(s => s.charAt(0).toUpperCase() + s.slice(1));
        const backgroundColors = [
            'rgba(75, 192, 192, 0.7)',   
            'rgba(255, 206, 86, 0.7)',   
            'rgba(255, 99, 132, 0.7)'    
        ];
        const borderColors = [
            'rgba(75, 192, 192, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(255, 99, 132, 1)'
        ];
        
        chartInstance = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Open Issues by Severity',
                    data: Object.values(severityCounts),
                    backgroundColor: backgroundColors,
                    borderColor: borderColors,
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            precision: 0
                        }
                    }
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `Open issues: ${context.parsed.y}`;
                            }
                        }
                    },
                    title: {
                        display: true,
                        text: 'Open Issues by Severity Level',
                        font: {
                            size: 16,
                            weight: 'bold'
                        }
                    }
                }
            }
        });
    }
    
    onDestroy(() => {
        if (chartInstance) {
            chartInstance.destroy();
        }
    });
</script>

{#if showModal}
    <div class="chart-modal" class:show={showModal}>
        <div class="chart-content">
            <div class="chart-header">
                <h3>Open Issues by Severity</h3>
                <button type="button" class="close-btn" on:click={closeModal}>&times;</button>
            </div>
            <div class="chart-body">
                <div class="chart-container">
                    <canvas id="severityChart"></canvas>
                </div>
                <div class="chart-summary">
                    <p>Issue & Insight Tracker</p>
                    {#if issues.filter(issue => issue.status === 'open').length === 0}
                        <p class="no-data">No open issues to display.</p>
                    {/if}
                </div>
            </div>
            <div class="chart-footer">
                <button type="button" class="btn btn-secondary" on:click={closeModal}>Close</button>
            </div>
        </div>
    </div>
{/if}

<style>
    .chart-modal {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
        opacity: 0;
        pointer-events: none;
        transition: opacity 0.3s ease;
    }
    
    .chart-modal.show {
        opacity: 1;
        pointer-events: auto;
    }
    
    .chart-content {
        background-color: white;
        border-radius: 8px;
        width: 90%;
        max-width: 700px;
        max-height: 90vh;
        overflow-y: auto;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
    }
    
    .chart-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem;
        border-bottom: 1px solid #e9ecef;
    }
    
    .chart-body {
        padding: 1rem;
    }
    
    .chart-container {
        height: 40vh;
        position: relative;
        margin-bottom: 1rem;
    }
    
    .chart-summary {
        padding: 0.5rem;
        font-size: 0.9rem;
        color: #666;
        text-align: center;
    }
    
    .no-data {
        font-style: italic;
        color: #999;
    }
    
    .chart-footer {
        padding: 1rem;
        border-top: 1px solid #e9ecef;
        text-align: right;
    }
    
    .close-btn {
        background: none;
        border: none;
        font-size: 1.5rem;
        cursor: pointer;
    }
</style>