# ============================================================
# main.py
# AutoCare Service Centre Management and Analysis System
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from vehicle_module import Vehicle, PremiumVehicle


# ============================================================
# SERVICE CHARGES
# ============================================================

SERVICE_PRICES = {
    "Engine Oil Change": 120.00,
    "Oil Filter Replacement": 35.00,
    "Brake Inspection": 50.00,
    "Air Filter Replacement": 45.00,
    "Tyre Rotation": 40.00,
    "Battery Check": 20.00,
    "Aircond Service": 150.00
}


# ============================================================
# FUNCTION 1
# Register Customer and Vehicle
# ============================================================

def register_customer(
    name,
    phone,
    registration_no,
    model,
    year=2026
):
    """
    Register customer and vehicle information.

    Default parameter:
    year = 2026
    """

    # Empty validation
    if not name.strip():
        raise ValueError("Customer name cannot be empty.")

    if not phone.strip():
        raise ValueError("Phone number cannot be empty.")

    if not registration_no.strip():
        raise ValueError(
            "Vehicle registration number cannot be empty."
        )

    if not model.strip():
        raise ValueError("Vehicle model cannot be empty.")

    # Phone validation
    phone_clean = phone.replace("-", "").replace(" ", "")

    if not phone_clean.isdigit():
        raise ValueError(
            "Phone number must contain digits only."
        )

    if len(phone_clean) < 10 or len(phone_clean) > 11:
        raise ValueError(
            "Phone number must contain 10 or 11 digits."
        )

    # Year range validation
    if year < 1990 or year > 2026:
        raise ValueError(
            "Vehicle year must be between 1990 and 2026."
        )

    # Create Vehicle object
    vehicle = Vehicle(
        owner_name=name.strip(),
        phone=phone_clean,
        registration_no=registration_no.strip().upper(),
        model=model.strip(),
        year=int(year)
    )

    return vehicle


# ============================================================
# FUNCTION 2
# Calculate Service Charge
# ============================================================

def calculate_service_charge(
    selected_services,
    discount=0.0
):
    """
    Calculate service charges.

    Default parameter:
    discount = 0.0

    This demonstrates the function overloading concept
    using default parameters.
    """

    # Empty service validation
    if not selected_services:
        raise ValueError(
            "Please select at least one service."
        )

    # Discount range validation
    if discount < 0 or discount > 100:
        raise ValueError(
            "Discount must be between 0% and 100%."
        )

    charges = {}

    # Calculate individual service charges
    for service in selected_services:

        if service not in SERVICE_PRICES:
            raise ValueError(
                f"Invalid service selected: {service}"
            )

        charges[service] = SERVICE_PRICES[service]

    # Calculate subtotal
    subtotal = sum(charges.values())

    # Calculate discount
    discount_amount = (
        subtotal * discount / 100
    )

    # Calculate final total
    total = subtotal - discount_amount

    return charges, subtotal, discount_amount, total


# ============================================================
# FUNCTION 3
# Display Customer and Vehicle Information
# ============================================================

def display_customer_vehicle_information(vehicle):
    """
    Display customer and vehicle information.
    """

    st.subheader(
        "👤 Customer & Vehicle Information"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            f"**Customer Name:** "
            f"{vehicle.owner_name}"
        )

        st.write(
            f"**Phone Number:** "
            f"{vehicle.phone}"
        )

        st.write(
            f"**Registration No.:** "
            f"{vehicle.registration_no}"
        )

    with col2:

        st.write(
            f"**Vehicle Model:** "
            f"{vehicle.model}"
        )

        st.write(
            f"**Vehicle Year:** "
            f"{vehicle.year}"
        )


# ============================================================
# STREAMLIT PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AutoCare Service Centre",
    page_icon="🚗",
    layout="wide"
)


# ============================================================
# PAGE HEADER
# ============================================================

st.title(
    "🚗 AutoCare Service Centre"
)

st.markdown(
    """
    ### Smart Car Service Centre Management and Analysis System

    Register customers, manage vehicle information,
    select services, calculate service charges,
    and analyse vehicle service data.
    """
)

st.divider()


# ============================================================
# CUSTOMER INFORMATION
# ============================================================

st.header("1️⃣ Customer Information")

customer_col1, customer_col2 = st.columns(2)

with customer_col1:

    name = st.text_input(
        "Customer Name",
        placeholder="Enter customer name"
    )

with customer_col2:

    phone = st.text_input(
        "Phone Number",
        placeholder="e.g. 0123456789"
    )


# ============================================================
# VEHICLE INFORMATION
# ============================================================

st.header("2️⃣ Vehicle Information")

vehicle_col1, vehicle_col2 = st.columns(2)

with vehicle_col1:

    registration_no = st.text_input(
        "Vehicle Registration Number",
        placeholder="e.g. PBA1234"
    )

    model = st.selectbox(
        "Vehicle Model",
        [
            "Perodua Myvi",
            "Perodua Axia",
            "Proton Saga",
            "Proton X50",
            "Other"
        ]
    )

with vehicle_col2:

    year = st.number_input(
        "Vehicle Year",
        min_value=1990,
        max_value=2026,
        value=2020,
        step=1
    )

    vehicle_type = st.selectbox(
        "Vehicle Type",
        [
            "Standard Vehicle",
            "Premium Vehicle"
        ]
    )


st.divider()


# ============================================================
# SERVICE SELECTION
# ============================================================

st.header("3️⃣ Select Vehicle Services")

selected_services = st.multiselect(
    "Choose one or more services:",
    options=list(SERVICE_PRICES.keys()),
    help="Select the services required by the customer."
)


# ============================================================
# AUTOMATIC SERVICE CHARGE DISPLAY
# ============================================================

if selected_services:

    st.subheader(
        "💰 Selected Service Charges"
    )

    preview_data = []

    for service in selected_services:

        preview_data.append(
            {
                "Service": service,
                "Service Charge (RM)": SERVICE_PRICES[service]
            }
        )

    preview_df = pd.DataFrame(
        preview_data
    )

    st.dataframe(
        preview_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "Select services above to view their charges."
    )


# ============================================================
# DISCOUNT
# ============================================================

st.subheader("Discount")

discount = st.number_input(
    "Discount (%)",
    min_value=0.0,
    max_value=100.0,
    value=0.0,
    step=5.0
)


st.divider()


# ============================================================
# CALCULATE & REGISTER BUTTON
# ============================================================

calculate_button = st.button(
    "🚗 Calculate & Register",
    type="primary",
    use_container_width=True
)


# ============================================================
# MAIN PROGRAM
# ============================================================

if calculate_button:

    try:

        # ----------------------------------------------------
        # CALL FUNCTION 1
        # Register customer and vehicle
        # ----------------------------------------------------

        vehicle = register_customer(
            name,
            phone,
            registration_no,
            model,
            year
        )


        # ----------------------------------------------------
        # Create PremiumVehicle object if selected
        # ----------------------------------------------------

        if vehicle_type == "Premium Vehicle":

            vehicle = PremiumVehicle(
                owner_name=vehicle.owner_name,
                phone=vehicle.phone,
                registration_no=vehicle.registration_no,
                model=vehicle.model,
                year=vehicle.year,
                membership="Gold"
            )


        # ----------------------------------------------------
        # CALL FUNCTION 2
        # Calculate service charges
        # ----------------------------------------------------

        (
            charges,
            subtotal,
            discount_amount,
            total
        ) = calculate_service_charge(
            selected_services,
            discount
        )


        # ----------------------------------------------------
        # Add services to Vehicle object
        # ----------------------------------------------------

        for service, charge in charges.items():

            vehicle.add_service(
                service,
                charge
            )


        # ----------------------------------------------------
        # CALL FUNCTION 3
        # Display customer and vehicle information
        # ----------------------------------------------------

        st.success(
            "Customer and vehicle registered successfully!"
        )

        display_customer_vehicle_information(
            vehicle
        )


        # ----------------------------------------------------
        # Display Vehicle / PremiumVehicle Object
        # ----------------------------------------------------

        st.subheader(
            "🚘 OOP Object Output"
        )

        if isinstance(
            vehicle,
            PremiumVehicle
        ):

            st.info(
                f"**Premium Vehicle Object**\n\n"
                f"{vehicle}\n\n"
                f"**Premium Benefit:** "
                f"{vehicle.premium_benefit()}"
            )

        else:

            st.info(
                f"**Vehicle Object**\n\n"
                f"{vehicle}"
            )


        # ----------------------------------------------------
        # SERVICE DETAILS
        # ----------------------------------------------------

        st.subheader(
            "🧾 Service Details"
        )

        service_data = []

        for service, charge in charges.items():

            service_data.append(
                {
                    "Service": service,
                    "Charge (RM)": charge
                }
            )

        service_df = pd.DataFrame(
            service_data
        )

        st.dataframe(
            service_df,
            use_container_width=True,
            hide_index=True
        )


        # ----------------------------------------------------
        # CHARGE SUMMARY
        # ----------------------------------------------------

        st.subheader(
            "💵 Charge Summary"
        )

        summary_col1, summary_col2, summary_col3 = st.columns(3)

        with summary_col1:

            st.metric(
                "Subtotal",
                f"RM {subtotal:.2f}"
            )

        with summary_col2:

            st.metric(
                "Discount",
                f"RM {discount_amount:.2f}"
            )

        with summary_col3:

            st.metric(
                "TOTAL CHARGE",
                f"RM {total:.2f}"
            )


        # ====================================================
        # NUMPY ANALYSIS
        # ====================================================

        st.divider()

        st.header(
            "📊 NumPy Analysis"
        )

        # Create NumPy array
        charge_array = np.array(
            list(charges.values()),
            dtype=float
        )


        # ----------------------------------------------------
        # Array Attributes
        # ----------------------------------------------------

        st.subheader(
            "NumPy Array Attributes"
        )

        numpy_col1, numpy_col2, numpy_col3, numpy_col4 = st.columns(4)

        with numpy_col1:

            st.metric(
                "Dimensions (ndim)",
                charge_array.ndim
            )

        with numpy_col2:

            st.metric(
                "Shape",
                str(charge_array.shape)
            )

        with numpy_col3:

            st.metric(
                "Size",
                charge_array.size
            )

        with numpy_col4:

            st.metric(
                "Data Type",
                str(charge_array.dtype)
            )


        # ----------------------------------------------------
        # Display Array
        # ----------------------------------------------------

        st.write(
            "**Service Charge Array:**"
        )

        st.write(
            charge_array
        )


        # ----------------------------------------------------
        # Indexing
        # ----------------------------------------------------

        st.write(
            "**Indexing:**"
        )

        if charge_array.size > 0:

            st.write(
                f"First service charge: "
                f"RM {charge_array[0]:.2f}"
            )


        # ----------------------------------------------------
        # Slicing
        # ----------------------------------------------------

        st.write(
            "**Slicing:**"
        )

        st.write(
            "First three service charges:",
            charge_array[:3]
        )


        # ----------------------------------------------------
        # Mathematical Analysis
        # ----------------------------------------------------

        st.subheader(
            "Mathematical Analysis"
        )

        math_col1, math_col2, math_col3, math_col4 = st.columns(4)

        with math_col1:

            st.metric(
                "Total",
                f"RM {np.sum(charge_array):.2f}"
            )

        with math_col2:

            st.metric(
                "Average",
                f"RM {np.mean(charge_array):.2f}"
            )

        with math_col3:

            st.metric(
                "Maximum",
                f"RM {np.max(charge_array):.2f}"
            )

        with math_col4:

            st.metric(
                "Minimum",
                f"RM {np.min(charge_array):.2f}"
            )


        # ====================================================
        # PANDAS ANALYSIS
        # ====================================================

        st.divider()

        st.header(
            "📋 Pandas Data Analysis"
        )


        # ----------------------------------------------------
        # DataFrame
        # ----------------------------------------------------

        st.subheader(
            "Service DataFrame"
        )

        st.dataframe(
            service_df,
            use_container_width=True,
            hide_index=True
        )


        # ----------------------------------------------------
        # Filtering
        # ----------------------------------------------------

        st.subheader(
            "🔎 Filtering"
        )

        filtered_df = service_df[
            service_df["Charge (RM)"] >= 50
        ]

        st.write(
            "Services with charges of RM50 or above:"
        )

        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True
        )


        # ----------------------------------------------------
        # Sorting
        # ----------------------------------------------------

        st.subheader(
            "↕️ Sorting"
        )

        sorted_df = service_df.sort_values(
            by="Charge (RM)",
            ascending=False
        )

        st.write(
            "Services sorted from highest to lowest charge:"
        )

        st.dataframe(
            sorted_df,
            use_container_width=True,
            hide_index=True
        )


        # ====================================================
        # MATPLOTLIB GRAPH
        # ====================================================

        st.divider()

        st.header(
            "📈 Service Charge Graph"
        )

        fig, ax = plt.subplots(
            figsize=(10, 5)
        )

        ax.bar(
            service_df["Service"],
            service_df["Charge (RM)"]
        )

        ax.set_title(
            "AutoCare Service Charges"
        )

        ax.set_xlabel(
            "Service"
        )

        ax.set_ylabel(
            "Charge (RM)"
        )

        ax.tick_params(
            axis="x",
            rotation=35
        )

        plt.tight_layout()

        st.pyplot(fig)


        # ====================================================
        # MAGIC METHODS & OPERATOR OVERLOADING DEMONSTRATION
        # ====================================================

        st.divider()

        st.header(
            "🧑‍💻 OOP & Magic Method Demonstration"
        )


        # ----------------------------------------------------
        # Create first Vehicle object
        # ----------------------------------------------------

        demo_vehicle_1 = Vehicle(
            owner_name="Demo Customer A",
            phone="0120000000",
            registration_no="DEMO001",
            model="Perodua Myvi",
            year=2020,
            service_charges={
                "Engine Oil Change": 120.00
            }
        )


        # ----------------------------------------------------
        # Create second Vehicle object
        # ----------------------------------------------------

        demo_vehicle_2 = Vehicle(
            owner_name="Demo Customer B",
            phone="0130000000",
            registration_no="DEMO002",
            model="Perodua Axia",
            year=2021,
            service_charges={
                "Brake Inspection": 50.00
            }
        )


        # ----------------------------------------------------
        # Create PremiumVehicle object
        # ----------------------------------------------------

        demo_premium = PremiumVehicle(
            owner_name="Premium Customer",
            phone="0140000000",
            registration_no="PREMIUM001",
            model="Proton X50",
            year=2024,
            service_charges={
                "Aircond Service": 150.00
            },
            membership="Gold"
        )


        # ----------------------------------------------------
        # __str__ demonstration
        # ----------------------------------------------------

        st.subheader(
            "1. __str__() Magic Method"
        )

        st.write(
            str(demo_vehicle_1)
        )


        # ----------------------------------------------------
        # Inheritance demonstration
        # ----------------------------------------------------

        st.subheader(
            "2. Inheritance - PremiumVehicle"
        )

        st.write(
            str(demo_premium)
        )

        st.write(
            f"Premium Benefit: "
            f"{demo_premium.premium_benefit()}"
        )


        # ----------------------------------------------------
        # __add__ Operator Overloading
        # ----------------------------------------------------

        st.subheader(
            "3. __add__() Operator Overloading"
        )

        combined_charge = (
            demo_vehicle_1 + demo_vehicle_2
        )

        st.write(
            f"Vehicle 1 Total: "
            f"RM {demo_vehicle_1.total_charge():.2f}"
        )

        st.write(
            f"Vehicle 2 Total: "
            f"RM {demo_vehicle_2.total_charge():.2f}"
        )

        st.success(
            f"Vehicle 1 + Vehicle 2 = "
            f"RM {combined_charge:.2f}"
        )


        # ----------------------------------------------------
        # Default Parameter / Function Overloading
        # ----------------------------------------------------

        st.subheader(
            "4. Default Parameter - Function Overloading"
        )

        no_discount_demo = calculate_service_charge(
            ["Engine Oil Change"]
        )

        ten_percent_demo = calculate_service_charge(
            ["Engine Oil Change"],
            10
        )

        st.write(
            "Without specifying discount:"
        )

        st.write(
            f"Total = RM "
            f"{no_discount_demo[3]:.2f}"
        )

        st.write(
            "With 10% discount:"
        )

        st.write(
            f"Total = RM "
            f"{ten_percent_demo[3]:.2f}"
        )


        # ====================================================
        # COMPLETION MESSAGE
        # ====================================================

        st.divider()

        st.success(
            "✅ AutoCare Service Centre processing completed successfully!"
        )


    # ========================================================
    # EXCEPTION HANDLING
    # ========================================================

    except ValueError as error:

        st.error(
            f"❌ Input Error: {error}"
        )

    except KeyError as error:

        st.error(
            f"❌ Service Error: {error}"
        )

    except TypeError as error:

        st.error(
            f"❌ Data Type Error: {error}"
        )

    except Exception as error:

        st.error(
            f"❌ Unexpected Error: {error}"
        )