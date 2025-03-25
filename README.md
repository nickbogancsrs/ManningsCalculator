# Manning's Flow Calculator

A web-based calculator for hydraulic flow calculations using Manning's equation. This tool helps engineers and hydrologists analyze flow in circular pipes, box culverts, and trapezoidal channels.

## Features

- **Circular Pipe Flow Calculator**: Calculate flow rate, velocity, and normal depth for partial or full pipe flow
- **Box Culvert Flow Calculator**: Analyze rectangular culvert hydraulics
- **Trapezoidal Channel Calculator**: Evaluate open channel flow characteristics
- **Size Determination**: Find the minimum required pipe or culvert size for a given design flow
- **Interactive Visualizations**: View rating curves for depth vs. flow and depth vs. velocity
- **Multiple Material Options**: Select from various materials with predefined roughness coefficients
- **Mobile-Friendly Design**: Responsive layout works on desktop and mobile devices

## How to Use

Visit the live site at: https://yourusername.github.io/mannings-flow-calculator/

### Circular Pipe Analysis
1. Select a pipe material or enter a custom Manning's n value
2. Enter pipe diameter and slope
3. Choose calculation type (full flow, partial flow, or find normal depth)
4. Click "Calculate" to see results and rating curve

### Box Culvert Analysis
1. Enter culvert width, height, and slope
2. Select calculation type
3. View results and hydraulic characteristics

### Trapezoidal Channel Analysis
1. Enter channel dimensions (bottom width and side slope)
2. Input slope and roughness
3. Calculate flow for a given depth or find normal depth for a given flow rate

### Size Determination
1. Enter design flow, slope, and material properties
2. Specify size constraints (minimum and maximum dimensions)
3. Find the smallest suitable size that can handle the design flow

## Development

### Technologies Used
- HTML5, CSS3, JavaScript
- Bootstrap 5 for responsive layout
- Plotly.js for interactive charts
- Math.js for numerical calculations

### Local Development

To run this project locally:

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/mannings-flow-calculator.git
   cd mannings-flow-calculator
   ```

2. Open `index.html` in your browser or use a local server.

### Deployment on GitHub Pages

To deploy your own version:

1. Fork this repository
2. Go to your fork's Settings > Pages
3. Select the main branch as the source
4. Your site will be available at https://yourusername.github.io/mannings-flow-calculator/

## Technical Details

### Manning's Equation

The calculator uses Manning's equation to determine flow characteristics:

V = (1.49/n) * R<sub>h</sub><sup>2/3</sup> * S<sup>1/2</sup>

Where:
- V is the cross-sectional average velocity (ft/s)
- n is Manning's roughness coefficient
- R<sub>h</sub> is the hydraulic radius (ft)
- S is the slope of the hydraulic grade line (ft/ft)

Flow rate is calculated as:

Q = V * A

Where:
- Q is the flow rate (cfs)
- A is the cross-sectional area of flow (ft²)

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Based on hydraulic engineering principles and Manning's equation
- CSS framework provided by Bootstrap
- Charts powered by Plotly.js
