                "Pipe diameter (ft):", 
                min_value=0.1, 
                max_value=20.0,
                value=3.0,
                step=0.1,
                key="pipe_diameter"
            )
            
            slope = st.number_input(
                "Channel slope (ft/ft):", 
                min_value=0.0001, 
                max_value=0.1, 
                value=0.01, 
                format="%.4f",
                key="pipe_slope"
            )
            
            calculation_type = st.radio(
                "Calculation type:",
                ["Full pipe flow", "Partial pipe flow", "Find normal depth for given flow"],
                key="pipe_calc_type"
            )
            
            if calculation_type == "Partial pipe flow":
                normal_depth = st.number_input(
                    "Flow depth (ft):", 
                    min_value=0.01, 
                    max_value=diameter, 
                    value=diameter/2,
                    step=0.1,
                    key="pipe_depth"
                )
            elif calculation_type == "Find normal depth for given flow":
                target_flow = st.number_input(
                    "Target flow (cfs):", 
                    min_value=0.1, 
                    value=10.0,
                    step=1.0,
                    key="pipe_target_flow"
                )
        
        with col2:
            # Calculate and display results
            if st.button("Calculate Pipe Flow", key="calc_pipe"):
                st.subheader("Results:")
                
                if calculation_type == "Full pipe flow":
                    result = calculator.calculate_circular_pipe_flow(diameter, slope, roughness)
                    st.write(f"Flow rate: {result['flow_cfs']:.2f} cfs")
                    st.write(f"Flow velocity: {result['velocity_fps']:.2f} ft/s")
                    st.write(f"Flow area: {result['area_sqft']:.2f} ft²")
                    
                elif calculation_type == "Partial pipe flow":
                    result = calculator.calculate_circular_pipe_flow(diameter, slope, roughness, normal_depth)
                    st.write(f"Flow rate: {result['flow_cfs']:.2f} cfs")
                    st.write(f"Flow velocity: {result['velocity_fps']:.2f} ft/s")
                    st.write(f"Flow area: {result['area_sqft']:.2f} ft²")
                    st.write(f"Percent full: {result['percent_full']:.1f}%")
                    st.write(f"Froude number: {result['froude_number']:.2f}")
                    
                    if result['froude_number'] < 1:
                        st.write("Flow regime: Subcritical")
                    elif result['froude_number'] > 1:
                        st.write("Flow regime: Supercritical")
                    else:
                        st.write("Flow regime: Critical")
                    
                else:  # Find normal depth
                    full_pipe = calculator.calculate_circular_pipe_flow(diameter, slope, roughness)
                    if target_flow > full_pipe['flow_cfs']:
                        st.error(f"Target flow exceeds full pipe capacity ({full_pipe['flow_cfs']:.2f} cfs)")
                    else:
                        normal_depth = calculator.find_normal_depth_circular(diameter, slope, roughness, target_flow)
                        st.write(f"Normal depth: {normal_depth:.2f} ft")
                        st.write(f"Percent full: {(normal_depth/diameter)*100:.1f}%")
                        
                        result = calculator.calculate_circular_pipe_flow(diameter, slope, roughness, normal_depth)
                        st.write(f"Flow velocity: {result['velocity_fps']:.2f} ft/s")
                        st.write(f"Froude number: {result['froude_number']:.2f}")
                
                # Plot rating curve
                st.subheader("Rating Curve:")
                fig = calculator.plot_rating_curve_circular(diameter, slope, roughness)
                st.pyplot(fig)
    
    # -------- Box Culvert Tab --------
    with tab2:
        st.header("Box Culvert Flow Calculator")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Input parameters
            material = st.selectbox(
                "Select culvert material:", 
                list(calculator.ROUGHNESS_COEFFICIENTS.keys()),
                format_func=lambda x: x.replace('_', ' ').title(),
                key="box_material"
            )
            custom_n = st.checkbox("Use custom roughness coefficient", key="box_custom_n")
            
            if custom_n:
                roughness = st.number_input(
                    "Manning's n value:", 
                    min_value=0.001, 
                    max_value=0.1, 
                    value=0.013, 
                    step=0.001,
                    format="%.3f",
                    key="box_roughness"
                )
            else:
                roughness = calculator.get_roughness_coefficient(material)
                st.write(f"Manning's n value: {roughness}")
            
            width = st.number_input(
                "Culvert width (ft):", 
                min_value=0.5, 
                max_value=30.0,
                value=6.0,
                step=0.5,
                key="box_width"
            )
            
            height = st.number_input(
                "Culvert height (ft):", 
                min_value=0.5, 
                max_value=20.0,
                value=4.0,
                step=0.5,
                key="box_height"
            )
            
            slope = st.number_input(
                "Channel slope (ft/ft):", 
                min_value=0.0001, 
                max_value=0.1, 
                value=0.01, 
                format="%.4f",
                key="box_slope"
            )
            
            calculation_type = st.radio(
                "Calculation type:",
                ["Full culvert flow", "Partial culvert flow", "Find normal depth for given flow"],
                key="box_calc_type"
            )
            
            if calculation_type == "Partial culvert flow":
                normal_depth = st.number_input(
                    "Flow depth (ft):", 
                    min_value=0.01, 
                    max_value=height, 
                    value=height/2,
                    step=0.1,
                    key="box_depth"
                )
            elif calculation_type == "Find normal depth for given flow":
                target_flow = st.number_input(
                    "Target flow (cfs):", 
                    min_value=0.1, 
                    value=50.0,
                    step=5.0,
                    key="box_target_flow"
                )
        
        with col2:
            # Calculate and display results
            if st.button("Calculate Box Culvert Flow", key="calc_box"):
                st.subheader("Results:")
                
                if calculation_type == "Full culvert flow":
                    result = calculator.calculate_box_culvert_flow(width, height, slope, roughness)
                    st.write(f"Flow rate: {result['flow_cfs']:.2f} cfs")
                    st.write(f"Flow velocity: {result['velocity_fps']:.2f} ft/s")
                    st.write(f"Flow area: {result['area_sqft']:.2f} ft²")
                    
                elif calculation_type == "Partial culvert flow":
                    result = calculator.calculate_box_culvert_flow(width, height, slope, roughness, normal_depth)
                    st.write(f"Flow rate: {result['flow_cfs']:.2f} cfs")
                    st.write(f"Flow velocity: {result['velocity_fps']:.2f} ft/s")
                    st.write(f"Flow area: {result['area_sqft']:.2f} ft²")
                    st.write(f"Percent full: {result['percent_full']:.1f}%")
                    st.write(f"Froude number: {result['froude_number']:.2f}")
                    
                    if result['froude_number'] < 1:
                        st.write("Flow regime: Subcritical")
                    elif result['froude_number'] > 1:
                        st.write("Flow regime: Supercritical")
                    else:
                        st.write("Flow regime: Critical")
                    
                else:  # Find normal depth
                    full_culvert = calculator.calculate_box_culvert_flow(width, height, slope, roughness)
                    if target_flow > full_culvert['flow_cfs']:
                        st.error(f"Target flow exceeds full culvert capacity ({full_culvert['flow_cfs']:.2f} cfs)")
                    else:
                        normal_depth = calculator.find_normal_depth_box(width, height, slope, roughness, target_flow)
                        st.write(f"Normal depth: {normal_depth:.2f} ft")
                        st.write(f"Percent full: {(normal_depth/height)*100:.1f}%")
                        
                        result = calculator.calculate_box_culvert_flow(width, height, slope, roughness, normal_depth)
                        st.write(f"Flow velocity: {result['velocity_fps']:.2f} ft/s")
                        st.write(f"Froude number: {result['froude_number']:.2f}")
                
                # Plot rating curve
                st.subheader("Rating Curve:")
                fig = calculator.plot_rating_curve_box(width, height, slope, roughness)
                st.pyplot(fig)
    
    # -------- Trapezoidal Channel Tab --------
    with tab3:
        st.header("Trapezoidal Channel Flow Calculator")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Input parameters
            material = st.selectbox(
                "Select channel material:", 
                list(calculator.ROUGHNESS_COEFFICIENTS.keys()),
                format_func=lambda x: x.replace('_', ' ').title(),
                key="channel_material"
            )
            custom_n = st.checkbox("Use custom roughness coefficient", key="channel_custom_n")
            
            if custom_n:
                roughness = st.number_input(
                    "Manning's n value:", 
                    min_value=0.001, 
                    max_value=0.1, 
                    value=0.03, 
                    step=0.001,
                    format="%.3f",
                    key="channel_roughness"
                )
            else:
                roughness = calculator.get_roughness_coefficient(material)
                st.write(f"Manning's n value: {roughness}")
            
            bottom_width = st.number_input(
                "Channel bottom width (ft):", 
                min_value=0.1, 
                max_value=50.0,
                value=10.0,
                step=1.0,
                key="channel_width"
            )
            
            side_slope = st.number_input(
                "Side slope (horizontal:1 vertical):", 
                min_value=0.1, 
                max_value=10.0,
                value=2.0,
                step=0.1,
                key="channel_side_slope"
            )
            
            slope = st.number_input(
                "Channel bed slope (ft/ft):", 
                min_value=0.0001, 
                max_value=0.1, 
                value=0.005, 
                format="%.4f",
                key="channel_slope"
            )
            
            calculation_type = st.radio(
                "Calculation type:",
                ["Calculate flow for given depth", "Find normal depth for given flow"],
                key="channel_calc_type"
            )
            
            if calculation_type == "Calculate flow for given depth":
                normal_depth = st.number_input(
                    "Flow depth (ft):", 
                    min_value=0.1, 
                    max_value=20.0, 
                    value=3.0,
                    step=0.1,
                    key="channel_depth"
                )
            else:  # Find normal depth
                target_flow = st.number_input(
                    "Target flow (cfs):", 
                    min_value=0.1, 
                    value=100.0,
                    step=10.0,
                    key="channel_target_flow"
                )
        
        with col2:
            # Calculate and display results
            if st.button("Calculate Channel Flow", key="calc_channel"):
                st.subheader("Results:")
                
                if calculation_type == "Calculate flow for given depth":
                    result = calculator.calculate_trapezoidal_channel_flow(
                        bottom_width, side_slope, slope, roughness, normal_depth
                    )
                    st.write(f"Flow rate: {result['flow_cfs']:.2f} cfs")
                    st.write(f"Flow velocity: {result['velocity_fps']:.2f} ft/s")
                    st.write(f"Flow area: {result['area_sqft']:.2f} ft²")
                    st.write(f"Top width: {result['top_width']:.2f} ft")
                    st.write(f"Froude number: {result['froude_number']:.2f}")
                    
                    if result['froude_number'] < 1:
                        st.write("Flow regime: Subcritical")
                    elif result['froude_number'] > 1:
                        st.write("Flow regime: Supercritical")
                    else:
                        st.write("Flow regime: Critical")
                    
                    if result['critical_depth'] is not None:
                        st.write(f"Critical depth: {result['critical_depth']:.2f} ft")
                    
                else:  # Find normal depth
                    normal_depth = calculator.find_normal_depth_trapezoidal(
                        bottom_width, side_slope, slope, roughness, target_flow
                    )
                    
                    st.write(f"Normal depth: {normal_depth:.2f} ft")
                    
                    result = calculator.calculate_trapezoidal_channel_flow(
                        bottom_width, side_slope, slope, roughness, normal_depth
                    )
                    
                    st.write(f"Flow velocity: {result['velocity_fps']:.2f} ft/s")
                    st.write(f"Flow area: {result['area_sqft']:.2f} ft²")
                    st.write(f"Top width: {result['top_width']:.2f} ft")
                    st.write(f"Froude number: {result['froude_number']:.2f}")
                    
                    if result['froude_number'] < 1:
                        st.write("Flow regime: Subcritical")
                    elif result['froude_number'] > 1:
                        st.write("Flow regime: Supercritical")
                    else:
                        st.write("Flow regime: Critical")
                
                # Plot rating curve
                st.subheader("Rating Curve:")
                fig = calculator.plot_rating_curve_trapezoidal(
                    bottom_width, side_slope, slope, roughness, max_depth=20
                )
                st.pyplot(fig)
    
    # -------- Size Determination Tab --------
    with tab4:
        st.header("Culvert Size Determination")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Input parameters
            culvert_type = st.radio(
                "Culvert type:",
                ["Circular Pipe", "Box Culvert"],
                key="size_culvert_type"
            )
            
            material = st.selectbox(
                "Select culvert material:", 
                list(calculator.ROUGHNESS_COEFFICIENTS.keys()),
                format_func=lambda x: x.replace('_', ' ').title(),
                key="size_material"
            )
            custom_n = st.checkbox("Use custom roughness coefficient", key="size_custom_n")
            
            if custom_n:
                roughness = st.number_input(
                    "Manning's n value:", 
                    min_value=0.001, 
                    max_value=0.1, 
                    value=0.013, 
                    step=0.001,
                    format="%.3f",
                    key="size_roughness"
                )
            else:
                roughness = calculator.get_roughness_coefficient(material)
                st.write(f"Manning's n value: {roughness}")
            
            slope = st.number_input(
                "Channel slope (ft/ft):", 
                min_value=0.0001, 
                max_value=0.1, 
                value=0.01, 
                format="%.4f",
                key="size_slope"
            )
            
            target_flow = st.number_input(
                "Design flow (cfs):", 
                min_value=0.1, 
                value=50.0,
                step=5.0,
                key="size_target_flow"
            )
            
            if culvert_type == "Circular Pipe":
                min_pipe_size = st.number_input(
                    "Minimum pipe diameter (ft):", 
                    min_value=0.5, 
                    max_value=5.0,
                    value=1.0,
                    step=0.5,
                    key="min_pipe_size"
                )
                
                max_pipe_size = st.number_input(
                    "Maximum pipe diameter (ft):", 
                    min_value=min_pipe_size + 0.5, 
                    max_value=20.0,
                    value=10.0,
                    step=0.5,
                    key="max_pipe_size"
                )
                
                pipe_increment = st.selectbox(
                    "Size increment (ft):", 
                    [0.25, 0.5, 1.0],
                    index=1,
                    key="pipe_increment"
                )
            
            else:  # Box Culvert
                min_width = st.number_input(
                    "Minimum culvert width (ft):", 
                    min_value=1.0, 
                    max_value=10.0,
                    value=2.0,
                    step=1.0,
                    key="min_width"
                )
                
                max_width = st.number_input(
                    "Maximum culvert width (ft):", 
                    min_value=min_width + 1.0, 
                    max_value=30.0,
                    value=20.0,
                    step=1.0,
                    key="max_width"
                )
                
                min_height = st.number_input(
                    "Minimum culvert height (ft):", 
                    min_value=1.0, 
                    max_value=10.0,
                    value=2.0,
                    step=1.0,
                    key="min_height"
                )
                
                max_height = st.number_input(
                    "Maximum culvert height (ft):", 
                    min_value=min_height + 1.0, 
                    max_value=20.0,
                    value=10.0,
                    step=1.0,
                    key="max_height"
                )
                
                box_increment = st.selectbox(
                    "Size increment (ft):", 
                    [0.5, 1.0, 2.0],
                    index=1,
                    key="box_increment"
                )
        
        with col2:
            # Calculate and display results
            if culvert_type == "Circular Pipe" and st.button("Find Minimum Pipe Size", key="find_pipe_size"):
                st.subheader("Results:")
                
                min_size = calculator.find_minimum_pipe_size(
                    slope, roughness, target_flow, 
                    min_size=min_pipe_size, 
                    max_size=max_pipe_size, 
                    increment=pipe_increment
                )
                
                if min_size is None:
                    st.error(f"No pipe size in the specified range can handle the design flow of {target_flow} cfs")
                else:
                    st.success(f"Minimum required pipe diameter: {min_size} ft")
                    
                    result = calculator.calculate_circular_pipe_flow(min_size, slope, roughness)
                    st.write(f"Flow capacity: {result['flow_cfs']:.2f} cfs")
                    st.write(f"Flow velocity: {result['velocity_fps']:.2f} ft/s")
                    
                    # Show normal depth for design flow
                    normal_depth = calculator.find_normal_depth_circular(min_size, slope, roughness, target_flow)
                    st.write(f"Normal depth for design flow: {normal_depth:.2f} ft")
                    st.write(f"Percent full at design flow: {(normal_depth/min_size)*100:.1f}%")
                    
                    # Plot rating curve
                    st.subheader("Rating Curve:")
                    fig = calculator.plot_rating_curve_circular(min_size, slope, roughness)
                    st.pyplot(fig)
            
            elif culvert_type == "Box Culvert" and st.button("Find Minimum Box Size", key="find_box_size"):
                st.subheader("Results:")
                
                min_size = calculator.find_minimum_box_size(
                    slope, roughness, target_flow, 
                    min_width=min_width, 
                    max_width=max_width,
                    min_height=min_height,
                    max_height=max_height,
                    increment=box_increment
                )
                
                if min_size is None:
                    st.error(f"No box size in the specified range can handle the design flow of {target_flow} cfs")
                else:
                    width = min_size['width']
                    height = min_size['height']
                    
                    st.success(f"Minimum required box culvert size: {width} ft × {height} ft")
                    
                    st.write(f"Flow capacity: {min_size['capacity']:.2f} cfs")
                    
                    # Show normal depth for design flow
                    normal_depth = calculator.find_normal_depth_box(width, height, slope, roughness, target_flow)
                    st.write(f"Normal depth for design flow: {normal_depth:.2f} ft")
                    st.write(f"Percent full at design flow: {(normal_depth/height)*100:.1f}%")
                    
                    # Plot rating curve
                    st.subheader("Rating Curve:")
                    fig = calculator.plot_rating_curve_box(width, height, slope, roughness)
                    st.pyplot(fig)
    
    # Footer information
    st.markdown("---")
    st.markdown("""
    ### About Manning's Equation
    
    Manning's equation is used to calculate the velocity of open-channel flow:
    
    $V = \\frac{1.49}{n} R_h^{2/3} S^{1/2}$
    
    Where:
    - $V$ is the cross-sectional average velocity (ft/s)
    - $n$ is Manning's roughness coefficient
    - $R_h$ is the hydraulic radius (ft)
    - $S$ is the slope of the hydraulic grade line (ft/ft)
    
    Flow rate is calculated by multiplying velocity by cross-sectional area:
    
    $Q = VA$
    
    This calculator handles circular pipes, rectangular box culverts, and trapezoidal channels.
    """)

if __name__ == "__main__":
    create_manning_app()
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize

class ManningsCalculator:
    """
    A calculator for Manning's equation to determine flow characteristics in
    culverts and open channels.
    """
    
    # Standard Manning's roughness coefficients
    ROUGHNESS_COEFFICIENTS = {
        'concrete_smooth': 0.012,
        'concrete_rough': 0.017,
        'corrugated_metal': 0.024,
        'hdpe_smooth': 0.010,
        'pvc': 0.009,
        'earth_clean': 0.022,
        'earth_with_gravel': 0.025,
        'natural_streams': 0.035,
        'rock_cut': 0.035,
        'brush': 0.050,
        'riprap': 0.035
    }
    
    def __init__(self):
        """Initialize the calculator"""
        pass
    
    def get_roughness_coefficient(self, material):
        """Get Manning's roughness coefficient for a given material"""
        return self.ROUGHNESS_COEFFICIENTS.get(material, 0.015)  # Default if not found
    
    def list_available_materials(self):
        """List all available materials and their roughness coefficients"""
        return self.ROUGHNESS_COEFFICIENTS
    
    def calculate_circular_pipe_flow(self, diameter, slope, roughness, normal_depth=None):
        """
        Calculate flow characteristics for a circular pipe
        
        Parameters:
        - diameter: pipe diameter in feet
        - slope: slope as a decimal (ft/ft)
        - roughness: Manning's n value
        - normal_depth: depth of flow in feet (if None, assumes full pipe)
        
        Returns:
        - Dictionary containing flow characteristics
        """
        # Convert to meters if needed for calculations
        radius = diameter / 2
        
        if normal_depth is None or normal_depth >= diameter:
            # Full pipe flow
            area = np.pi * radius**2
            wetted_perimeter = 2 * np.pi * radius
            hydraulic_radius = area / wetted_perimeter
            
            # Calculate velocity using Manning's equation
            velocity = (1.49 / roughness) * hydraulic_radius**(2/3) * slope**(1/2)
            flow = velocity * area
            
            return {
                'flow_cfs': flow,
                'velocity_fps': velocity,
                'area_sqft': area,
                'full_capacity': True,
                'percent_full': 100.0,
                'critical_depth': None,
                'froude_number': None
            }
        
        else:
            # Partially full pipe
            # Calculate geometric properties for partial pipe
            theta = 2 * np.arccos((radius - normal_depth) / radius)
            area = (radius**2) * (theta - np.sin(theta)) / 2
            wetted_perimeter = radius * theta
            
            if wetted_perimeter == 0:
                return {
                    'flow_cfs': 0,
                    'velocity_fps': 0,
                    'area_sqft': 0,
                    'full_capacity': False,
                    'percent_full': 0,
                    'critical_depth': 0,
                    'froude_number': 0
                }
                
            hydraulic_radius = area / wetted_perimeter
            
            # Calculate velocity using Manning's equation
            velocity = (1.49 / roughness) * hydraulic_radius**(2/3) * slope**(1/2)
            flow = velocity * area
            
            # Calculate percent full
            full_area = np.pi * radius**2
            percent_full = (area / full_area) * 100
            
            # Calculate critical depth and Froude number
            g = 32.2  # acceleration due to gravity in ft/s²
            top_width = 2 * np.sqrt(normal_depth * (diameter - normal_depth))
            froude = velocity / np.sqrt(g * (area / top_width))
            
            # Simple approximation for critical depth in circular pipe
            critical_depth = (flow**2 / (g * top_width))**(1/3)
            
            return {
                'flow_cfs': flow,
                'velocity_fps': velocity,
                'area_sqft': area,
                'full_capacity': False,
                'percent_full': percent_full,
                'normal_depth': normal_depth,
                'critical_depth': critical_depth,
                'froude_number': froude
            }
    
    def calculate_box_culvert_flow(self, width, height, slope, roughness, normal_depth=None):
        """
        Calculate flow characteristics for a rectangular box culvert
        
        Parameters:
        - width: culvert width in feet
        - height: culvert height in feet
        - slope: slope as a decimal (ft/ft)
        - roughness: Manning's n value
        - normal_depth: depth of flow in feet (if None, assumes full culvert)
        
        Returns:
        - Dictionary containing flow characteristics
        """
        if normal_depth is None or normal_depth >= height:
            # Full culvert flow
            area = width * height
            wetted_perimeter = 2 * (width + height)
            hydraulic_radius = area / wetted_perimeter
            
            # Calculate velocity using Manning's equation
            velocity = (1.49 / roughness) * hydraulic_radius**(2/3) * slope**(1/2)
            flow = velocity * area
            
            return {
                'flow_cfs': flow,
                'velocity_fps': velocity,
                'area_sqft': area,
                'full_capacity': True,
                'percent_full': 100.0,
                'critical_depth': None,
                'froude_number': None
            }
        
        else:
            # Partially full culvert
            area = width * normal_depth
            wetted_perimeter = width + 2 * normal_depth
            hydraulic_radius = area / wetted_perimeter
            
            # Calculate velocity using Manning's equation
            velocity = (1.49 / roughness) * hydraulic_radius**(2/3) * slope**(1/2)
            flow = velocity * area
            
            # Calculate percent full
            full_area = width * height
            percent_full = (area / full_area) * 100
            
            # Calculate critical depth and Froude number
            g = 32.2  # acceleration due to gravity in ft/s²
            top_width = width  # For rectangular channel, top width is constant
            froude = velocity / np.sqrt(g * normal_depth)
            critical_depth = (flow**2 / (g * width**2))**(1/3)
            
            return {
                'flow_cfs': flow,
                'velocity_fps': velocity,
                'area_sqft': area,
                'full_capacity': False,
                'percent_full': percent_full,
                'normal_depth': normal_depth,
                'critical_depth': critical_depth,
                'froude_number': froude
            }
    
    def calculate_trapezoidal_channel_flow(self, bottom_width, side_slope, slope, roughness, normal_depth):
        """
        Calculate flow characteristics for a trapezoidal channel
        
        Parameters:
        - bottom_width: channel bottom width in feet
        - side_slope: horizontal to vertical ratio (e.g., 2 means 2H:1V)
        - slope: channel bed slope as a decimal (ft/ft)
        - roughness: Manning's n value
        - normal_depth: depth of flow in feet
        
        Returns:
        - Dictionary containing flow characteristics
        """
        if normal_depth <= 0:
            return {
                'flow_cfs': 0,
                'velocity_fps': 0,
                'area_sqft': 0
            }
        
        # Calculate geometric properties
        area = (bottom_width + side_slope * normal_depth) * normal_depth
        wetted_perimeter = bottom_width + 2 * normal_depth * np.sqrt(1 + side_slope**2)
        hydraulic_radius = area / wetted_perimeter
        
        # Calculate velocity using Manning's equation
        velocity = (1.49 / roughness) * hydraulic_radius**(2/3) * slope**(1/2)
        flow = velocity * area
        
        # Calculate critical depth and Froude number
        g = 32.2  # acceleration due to gravity in ft/s²
        top_width = bottom_width + 2 * side_slope * normal_depth
        froude = velocity / np.sqrt(g * normal_depth)
        
        # Approximation for critical depth in trapezoidal channel
        def critical_depth_equation(y):
            A = (bottom_width + side_slope * y) * y
            T = bottom_width + 2 * side_slope * y
            return A**3 / T - flow**2 / g
        
        try:
            critical_depth = optimize.brentq(critical_depth_equation, 0.01, 100, maxiter=100)
        except ValueError:
            critical_depth = None
        
        return {
            'flow_cfs': flow,
            'velocity_fps': velocity,
            'area_sqft': area,
            'normal_depth': normal_depth,
            'critical_depth': critical_depth,
            'froude_number': froude,
            'top_width': top_width
        }
    
    def find_normal_depth_circular(self, diameter, slope, roughness, target_flow):
        """
        Find the normal depth for a given flow in a circular pipe
        
        Parameters:
        - diameter: pipe diameter in feet
        - slope: slope as a decimal (ft/ft)
        - roughness: Manning's n value
        - target_flow: flow rate in cfs
        
        Returns:
        - Normal depth in feet
        """
        # First check if the flow exceeds full pipe capacity
        full_pipe = self.calculate_circular_pipe_flow(diameter, slope, roughness)
        if target_flow > full_pipe['flow_cfs']:
            return None  # Flow exceeds capacity
        
        def flow_difference(depth):
            result = self.calculate_circular_pipe_flow(diameter, slope, roughness, depth)
            return result['flow_cfs'] - target_flow
        
        try:
            # Use numerical methods to find the depth that gives the target flow
            normal_depth = optimize.brentq(flow_difference, 0.01, diameter, maxiter=100)
            return normal_depth
        except (ValueError, RuntimeError):
            # If the numerical method fails, use a brute force approach
            depths = np.linspace(0.01, diameter, 100)
            flows = [self.calculate_circular_pipe_flow(diameter, slope, roughness, d)['flow_cfs'] for d in depths]
            idx = np.abs(np.array(flows) - target_flow).argmin()
            return depths[idx]
    
    def find_normal_depth_box(self, width, height, slope, roughness, target_flow):
        """
        Find the normal depth for a given flow in a box culvert
        
        Parameters:
        - width: culvert width in feet
        - height: culvert height in feet
        - slope: slope as a decimal (ft/ft)
        - roughness: Manning's n value
        - target_flow: flow rate in cfs
        
        Returns:
        - Normal depth in feet
        """
        # First check if the flow exceeds full culvert capacity
        full_culvert = self.calculate_box_culvert_flow(width, height, slope, roughness)
        if target_flow > full_culvert['flow_cfs']:
            return None  # Flow exceeds capacity
        
        def flow_difference(depth):
            result = self.calculate_box_culvert_flow(width, height, slope, roughness, depth)
            return result['flow_cfs'] - target_flow
        
        try:
            # Use numerical methods to find the depth that gives the target flow
            normal_depth = optimize.brentq(flow_difference, 0.01, height, maxiter=100)
            return normal_depth
        except (ValueError, RuntimeError):
            # If the numerical method fails, use a brute force approach
            depths = np.linspace(0.01, height, 100)
            flows = [self.calculate_box_culvert_flow(width, height, slope, roughness, d)['flow_cfs'] for d in depths]
            idx = np.abs(np.array(flows) - target_flow).argmin()
            return depths[idx]
    
    def find_normal_depth_trapezoidal(self, bottom_width, side_slope, slope, roughness, target_flow, max_depth=20):
        """
        Find the normal depth for a given flow in a trapezoidal channel
        
        Parameters:
        - bottom_width: channel bottom width in feet
        - side_slope: horizontal to vertical ratio (e.g., 2 means 2H:1V)
        - slope: channel bed slope as a decimal (ft/ft)
        - roughness: Manning's n value
        - target_flow: flow rate in cfs
        - max_depth: maximum depth to consider in feet
        
        Returns:
        - Normal depth in feet
        """
        def flow_difference(depth):
            result = self.calculate_trapezoidal_channel_flow(bottom_width, side_slope, slope, roughness, depth)
            return result['flow_cfs'] - target_flow
        
        try:
            # Use numerical methods to find the depth that gives the target flow
            normal_depth = optimize.brentq(flow_difference, 0.01, max_depth, maxiter=100)
            return normal_depth
        except (ValueError, RuntimeError):
            # If the numerical method fails, use a brute force approach
            depths = np.linspace(0.01, max_depth, 100)
            flows = [self.calculate_trapezoidal_channel_flow(bottom_width, side_slope, slope, roughness, d)['flow_cfs'] for d in depths]
            idx = np.abs(np.array(flows) - target_flow).argmin()
            return depths[idx]
    
    def find_minimum_pipe_size(self, slope, roughness, target_flow, min_size=0.5, max_size=10, increment=0.5):
        """
        Find the minimum pipe size that can handle a given flow
        
        Parameters:
        - slope: slope as a decimal (ft/ft)
        - roughness: Manning's n value
        - target_flow: flow rate in cfs
        - min_size: minimum pipe diameter to consider in feet
        - max_size: maximum pipe diameter to consider in feet
        - increment: size increment to check in feet
        
        Returns:
        - Minimum required pipe diameter in feet
        """
        sizes = np.arange(min_size, max_size + increment, increment)
        for size in sizes:
            flow_capacity = self.calculate_circular_pipe_flow(size, slope, roughness)['flow_cfs']
            if flow_capacity >= target_flow:
                return size
        
        return None  # No size in the range can handle the flow
    
    def find_minimum_box_size(self, slope, roughness, target_flow, min_width=1, max_width=20, min_height=1, max_height=20, increment=1):
        """
        Find a suitable box culvert size that can handle a given flow
        
        Parameters:
        - slope: slope as a decimal (ft/ft)
        - roughness: Manning's n value
        - target_flow: flow rate in cfs
        - min_width: minimum culvert width to consider in feet
        - max_width: maximum culvert width to consider in feet
        - min_height: minimum culvert height to consider in feet
        - max_height: maximum culvert height to consider in feet
        - increment: size increment to check in feet
        
        Returns:
        - Dictionary with width and height of minimum suitable box culvert
        """
        # Try to find a size with a reasonable width-to-height ratio (1:1 to 3:1)
        suitable_sizes = []
        
        for width in np.arange(min_width, max_width + increment, increment):
            for height in np.arange(min_height, max_height + increment, increment):
                if width / height > 3 or height > width:
                    continue  # Skip unreasonable proportions
                
                flow_capacity = self.calculate_box_culvert_flow(width, height, slope, roughness)['flow_cfs']
                
                if flow_capacity >= target_flow:
                    suitable_sizes.append({
                        'width': width,
                        'height': height,
                        'area': width * height,
                        'capacity': flow_capacity
                    })
        
        if not suitable_sizes:
            return None  # No size in the range can handle the flow
        
        # Find the smallest culvert by area
        suitable_sizes.sort(key=lambda x: x['area'])
        return suitable_sizes[0]
    
    def plot_rating_curve_circular(self, diameter, slope, roughness, max_depth=None):
        """
        Generate a rating curve for a circular pipe
        
        Parameters:
        - diameter: pipe diameter in feet
        - slope: slope as a decimal (ft/ft)
        - roughness: Manning's n value
        - max_depth: maximum depth to consider (defaults to diameter)
        
        Returns:
        - Matplotlib figure object
        """
        if max_depth is None:
            max_depth = diameter
            
        depths = np.linspace(0.01, max_depth, 50)
        flows = []
        velocities = []
        
        for depth in depths:
            result = self.calculate_circular_pipe_flow(diameter, slope, roughness, depth)
            flows.append(result['flow_cfs'])
            velocities.append(result['velocity_fps'])
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Plot depth vs flow
        ax1.plot(flows, depths, 'b-')
        ax1.set_xlabel('Flow (cfs)')
        ax1.set_ylabel('Depth (ft)')
        ax1.set_title(f'Rating Curve for {diameter}ft Circular Pipe\nSlope = {slope}, n = {roughness}')
        ax1.grid(True)
        
        # Plot depth vs velocity
        ax2.plot(velocities, depths, 'r-')
        ax2.set_xlabel('Velocity (ft/s)')
        ax2.set_ylabel('Depth (ft)')
        ax2.set_title(f'Velocity Profile for {diameter}ft Circular Pipe\nSlope = {slope}, n = {roughness}')
        ax2.grid(True)
        
        plt.tight_layout()
        return fig
    
    def plot_rating_curve_box(self, width, height, slope, roughness, max_depth=None):
        """
        Generate a rating curve for a box culvert
        
        Parameters:
        - width: culvert width in feet
        - height: culvert height in feet
        - slope: slope as a decimal (ft/ft)
        - roughness: Manning's n value
        - max_depth: maximum depth to consider (defaults to height)
        
        Returns:
        - Matplotlib figure object
        """
        if max_depth is None:
            max_depth = height
            
        depths = np.linspace(0.01, max_depth, 50)
        flows = []
        velocities = []
        
        for depth in depths:
            result = self.calculate_box_culvert_flow(width, height, slope, roughness, depth)
            flows.append(result['flow_cfs'])
            velocities.append(result['velocity_fps'])
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Plot depth vs flow
        ax1.plot(flows, depths, 'b-')
        ax1.set_xlabel('Flow (cfs)')
        ax1.set_ylabel('Depth (ft)')
        ax1.set_title(f'Rating Curve for {width}ft x {height}ft Box Culvert\nSlope = {slope}, n = {roughness}')
        ax1.grid(True)
        
        # Plot depth vs velocity
        ax2.plot(velocities, depths, 'r-')
        ax2.set_xlabel('Velocity (ft/s)')
        ax2.set_ylabel('Depth (ft)')
        ax2.set_title(f'Velocity Profile for {width}ft x {height}ft Box Culvert\nSlope = {slope}, n = {roughness}')
        ax2.grid(True)
        
        plt.tight_layout()
        return fig
    
    def plot_rating_curve_trapezoidal(self, bottom_width, side_slope, slope, roughness, max_depth=10):
        """
        Generate a rating curve for a trapezoidal channel
        
        Parameters:
        - bottom_width: channel bottom width in feet
        - side_slope: horizontal to vertical ratio (e.g., 2 means 2H:1V)
        - slope: channel bed slope as a decimal (ft/ft)
        - roughness: Manning's n value
        - max_depth: maximum depth to consider in feet
        
        Returns:
        - Matplotlib figure object
        """
        depths = np.linspace(0.01, max_depth, 50)
        flows = []
        velocities = []
        froude_numbers = []
        
        for depth in depths:
            result = self.calculate_trapezoidal_channel_flow(bottom_width, side_slope, slope, roughness, depth)
            flows.append(result['flow_cfs'])
            velocities.append(result['velocity_fps'])
            froude_numbers.append(result['froude_number'])
        
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
        
        # Plot depth vs flow
        ax1.plot(flows, depths, 'b-')
        ax1.set_xlabel('Flow (cfs)')
        ax1.set_ylabel('Depth (ft)')
        ax1.set_title(f'Rating Curve for Trapezoidal Channel\nBottom Width = {bottom_width}ft, Side Slope = {side_slope}:1')
        ax1.grid(True)
        
        # Plot depth vs velocity
        ax2.plot(velocities, depths, 'r-')
        ax2.set_xlabel('Velocity (ft/s)')
        ax2.set_ylabel('Depth (ft)')
        ax2.set_title(f'Velocity Profile\nSlope = {slope}, n = {roughness}')
        ax2.grid(True)
        
        # Plot depth vs Froude number
        ax3.plot(froude_numbers, depths, 'g-')
        ax3.axvline(x=1, color='k', linestyle='--', alpha=0.7)
        ax3.set_xlabel('Froude Number')
        ax3.set_ylabel('Depth (ft)')
        ax3.set_title('Flow Regime')
        ax3.grid(True)
        
        plt.tight_layout()
        return fig

# Create a web application for the calculator
import streamlit as st

def create_manning_app():
    st.set_page_config(page_title="Manning's Flow Calculator", layout="wide")
    st.title("Manning's Flow Calculator for Culverts and Channels")
    
    calculator = ManningsCalculator()
    
    # Create tabs for different calculation types
    tab1, tab2, tab3, tab4 = st.tabs([
        "Circular Pipe", 
        "Box Culvert", 
        "Trapezoidal Channel", 
        "Size Determination"
    ])
    
    # -------- Circular Pipe Tab --------
    with tab1:
        st.header("Circular Pipe Flow Calculator")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Input parameters
            material = st.selectbox(
                "Select pipe material:", 
                list(calculator.ROUGHNESS_COEFFICIENTS.keys()),
                format_func=lambda x: x.replace('_', ' ').title(),
                key="pipe_material"
            )
            custom_n = st.checkbox("Use custom roughness coefficient", key="pipe_custom_n")
            
            if custom_n:
                roughness = st.number_input(
                    "Manning's n value:", 
                    min_value=0.001, 
                    max_value=0.1, 
                    value=0.013, 
                    step=0.001,
                    format="%.3f",
                    key="pipe_roughness"
                )
            else:
                roughness = calculator.get_roughness_coefficient(material)
                st.write(f"Manning's n value: {roughness}")
            
            diameter = st.number_input(
                "Pipe diameter (ft):", 
                min_value=0.1, 
                max_value=20.0