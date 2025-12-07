# scripts/seed_firestore_manual.py

import sys
import os

# Make sure app package is importable
sys.path.append(os.getcwd())

from app.firebase import db

"""
We will seed 70 schemes:

Sectors (category field):
- Agriculture
- Education
- Finance
- Food
- Health
- Power & Energy
- Labour & Employment

For each sector: 
- 7 Karnataka state schemes  (level = "state", state = "Karnataka")
- 3 Central schemes          (level = "central", state = "India")
"""

SCHEMES = [
    # =========================
    # 1. AGRICULTURE (10)
    # =========================

    # Karnataka (7)
    {
        "id": "ka_agri_raitha_siri_income_support",
        "name": "Raitha Siri Income Support",
        "level": "state",
        "state": "Karnataka",
        "category": "Agriculture",
        "eligibility": "Small and marginal farmers in Karnataka with valid land records.",
        "benefits": "Direct income support per acre of cultivated land to eligible farmers.",
        "apply_link": "https://services.karnataka.gov.in/raitha-siri"
    },
    {
        "id": "ka_agri_krishi_bhagya_irrigation",
        "name": "Krishi Bhagya Irrigation Support",
        "level": "state",
        "state": "Karnataka",
        "category": "Agriculture",
        "eligibility": "Farmers in dryland areas of Karnataka.",
        "benefits": "Subsidy for farm ponds, diesel pumps, and micro-irrigation structures.",
        "apply_link": "https://services.karnataka.gov.in/krishi-bhagya"
    },
    {
        "id": "ka_agri_bhoo_siri_organic",
        "name": "Bhoo Siri Organic Farming Support",
        "level": "state",
        "state": "Karnataka",
        "category": "Agriculture",
        "eligibility": "Farmers adopting organic cultivation or millets.",
        "benefits": "Assistance for organic inputs, certification, and training.",
        "apply_link": "https://services.karnataka.gov.in/bhoo-siri"
    },
    {
        "id": "ka_agri_machinery_subsidy",
        "name": "Farm Machinery Subsidy Scheme",
        "level": "state",
        "state": "Karnataka",
        "category": "Agriculture",
        "eligibility": "Registered farmers in Karnataka.",
        "benefits": "Subsidy on purchase of tractors, power tillers and small machinery.",
        "apply_link": "https://services.karnataka.gov.in/farm-machinery"
    },
    {
        "id": "ka_agri_dryland_support",
        "name": "Dryland Farmer Support Scheme",
        "level": "state",
        "state": "Karnataka",
        "category": "Agriculture",
        "eligibility": "Farmers cultivating in drought-prone taluks.",
        "benefits": "Input subsidy and drought relief assistance.",
        "apply_link": "https://services.karnataka.gov.in/dryland-support"
    },
    {
        "id": "ka_agri_horticulture_mission",
        "name": "Horticulture Expansion Mission",
        "level": "state",
        "state": "Karnataka",
        "category": "Agriculture",
        "eligibility": "Farmers interested in fruits, vegetables and plantation crops.",
        "benefits": "Subsidy for saplings, drip irrigation and pack houses.",
        "apply_link": "https://services.karnataka.gov.in/horticulture"
    },
    {
        "id": "ka_agri_dairy_farmer_incentive",
        "name": "Dairy Farmer Incentive Scheme",
        "level": "state",
        "state": "Karnataka",
        "category": "Agriculture",
        "eligibility": "Members of cooperative milk societies in Karnataka.",
        "benefits": "Per-litre incentive for milk poured into cooperative societies.",
        "apply_link": "https://services.karnataka.gov.in/dairy-incentive"
    },

    # Central (3)
    {
        "id": "cen_agri_pm_kisan",
        "name": "PM-KISAN Samman Nidhi",
        "level": "central",
        "state": "India",
        "category": "Agriculture",
        "eligibility": "Small and marginal farmers with cultivable land.",
        "benefits": "₹6,000 per year in 3 installments directly to bank account.",
        "apply_link": "https://pmkisan.gov.in"
    },
    {
        "id": "cen_agri_pm_fasal_bima",
        "name": "Pradhan Mantri Fasal Bima Yojana",
        "level": "central",
        "state": "India",
        "category": "Agriculture",
        "eligibility": "Farmers growing notified crops in notified areas.",
        "benefits": "Crop insurance against yield losses due to natural calamities.",
        "apply_link": "https://pmfby.gov.in"
    },
    {
        "id": "cen_agri_agri_infra_fund",
        "name": "Agriculture Infrastructure Fund",
        "level": "central",
        "state": "India",
        "category": "Agriculture",
        "eligibility": "Farmers, FPOs, cooperatives and startups in agriculture.",
        "benefits": "Interest subvention and credit guarantee for agri-infrastructure projects.",
        "apply_link": "https://www.agriinfra.dac.gov.in"
    },

    # =========================
    # 2. EDUCATION (10)
    # =========================

    # Karnataka (7)
    {
        "id": "ka_edu_vidyasiri_hostel",
        "name": "Vidyasiri Hostel Scholarship",
        "level": "state",
        "state": "Karnataka",
        "category": "Education",
        "eligibility": "Backward class students studying in post-matric courses.",
        "benefits": "Hostel fees and stipend support for higher education.",
        "apply_link": "https://karepass.cgg.gov.in"
    },
    {
        "id": "ka_edu_pre_matric_scst",
        "name": "Pre-Matric Scholarship for SC/ST Students",
        "level": "state",
        "state": "Karnataka",
        "category": "Education",
        "eligibility": "SC/ST students from class 1 to 10 in Karnataka.",
        "benefits": "Scholarship to cover school expenses and books.",
        "apply_link": "https://sscholarship.karnataka.gov.in"
    },
    {
        "id": "ka_edu_post_matric_scst",
        "name": "Post-Matric Scholarship for SC/ST Students",
        "level": "state",
        "state": "Karnataka",
        "category": "Education",
        "eligibility": "SC/ST students pursuing PU, UG or PG courses.",
        "benefits": "Tuition fee reimbursement and maintenance allowance.",
        "apply_link": "https://sscholarship.karnataka.gov.in"
    },
    {
        "id": "ka_edu_girl_child_higher_edu",
        "name": "Girl Child Higher Education Support",
        "level": "state",
        "state": "Karnataka",
        "category": "Education",
        "eligibility": "Girls from low-income households enrolling in degree courses.",
        "benefits": "Scholarship and fee concessions for higher education.",
        "apply_link": "https://services.karnataka.gov.in/girl-education"
    },
    {
        "id": "ka_edu_rural_student_laptop",
        "name": "Rural Student Digital Access Scheme",
        "level": "state",
        "state": "Karnataka",
        "category": "Education",
        "eligibility": "Rural students enrolled in government colleges.",
        "benefits": "Subsidized laptops or tablets for digital learning.",
        "apply_link": "https://services.karnataka.gov.in/digital-student"
    },
    {
        "id": "ka_edu_minority_merit",
        "name": "Minority Merit Scholarship",
        "level": "state",
        "state": "Karnataka",
        "category": "Education",
        "eligibility": "Meritorious students from notified minority communities.",
        "benefits": "Scholarship for tuition and exam fees.",
        "apply_link": "https://gokdom.karnataka.gov.in"
    },
    {
        "id": "ka_edu_free_bus_pass",
        "name": "Free Bus Pass for Students",
        "level": "state",
        "state": "Karnataka",
        "category": "Education",
        "eligibility": "Students commuting to schools/colleges by KSRTC/BMTC buses.",
        "benefits": "Free or concessional travel passes for students.",
        "apply_link": "https://sevasindhu.karnataka.gov.in"
    },

    # Central (3)
    {
        "id": "cen_edu_nmms",
        "name": "National Means-cum-Merit Scholarship",
        "level": "central",
        "state": "India",
        "category": "Education",
        "eligibility": "Class 8 students from low-income families in government schools.",
        "benefits": "Annual scholarship to reduce dropouts at secondary stage.",
        "apply_link": "https://scholarships.gov.in"
    },
    {
        "id": "cen_edu_top_class_sc",
        "name": "Top Class Education Scheme for SC Students",
        "level": "central",
        "state": "India",
        "category": "Education",
        "eligibility": "SC students admitted to notified premier institutions.",
        "benefits": "Full tuition fee, living allowance and computer/laptop support.",
        "apply_link": "https://scholarships.gov.in"
    },
    {
        "id": "cen_edu_aicte_pragati_girls",
        "name": "AICTE Pragati Scholarship for Girl Students",
        "level": "central",
        "state": "India",
        "category": "Education",
        "eligibility": "Girl students in first year of technical degree or diploma.",
        "benefits": "Scholarship amount per year towards tuition and incidental charges.",
        "apply_link": "https://www.aicte-pragati-saksham.gov.in"
    },

    # =========================
    # 3. FINANCE (10)
    # =========================

    # Karnataka (7)
    {
        "id": "ka_fin_yuva_nidhi",
        "name": "Yuva Nidhi Unemployment Allowance",
        "level": "state",
        "state": "Karnataka",
        "category": "Finance",
        "eligibility": "Unemployed graduates and diploma holders registered in Karnataka.",
        "benefits": "Monthly allowance credited directly to beneficiary accounts.",
        "apply_link": "https://sevasindhu.karnataka.gov.in/yuva-nidhi"
    },
    {
        "id": "ka_fin_stree_samarthya",
        "name": "Stree Samarthya SHG Loan Support",
        "level": "state",
        "state": "Karnataka",
        "category": "Finance",
        "eligibility": "Women self-help groups and federations.",
        "benefits": "Interest subvention and credit linkage for SHG enterprises.",
        "apply_link": "https://ksrlm.karnataka.gov.in"
    },
    {
        "id": "ka_fin_micro_enterprise_credit",
        "name": "Micro-Enterprise Credit Support Scheme",
        "level": "state",
        "state": "Karnataka",
        "category": "Finance",
        "eligibility": "First-generation entrepreneurs with viable small business plans.",
        "benefits": "Subsidized loans through banks and cooperative societies.",
        "apply_link": "https://services.karnataka.gov.in/micro-enterprise"
    },
    {
        "id": "ka_fin_farmer_interest_subvention",
        "name": "Farmer Interest Subvention Scheme",
        "level": "state",
        "state": "Karnataka",
        "category": "Finance",
        "eligibility": "Farmers availing crop loans from scheduled banks.",
        "benefits": "Interest subsidy on timely repayment of crop loans.",
        "apply_link": "https://services.karnataka.gov.in/farmer-interest"
    },
    {
        "id": "ka_fin_street_vendor_loan",
        "name": "Street Vendor Soft Loan Scheme",
        "level": "state",
        "state": "Karnataka",
        "category": "Finance",
        "eligibility": "Registered urban street vendors.",
        "benefits": "Small working capital loans at concessional interest.",
        "apply_link": "https://services.karnataka.gov.in/street-vendor"
    },
    {
        "id": "ka_fin_self_employment_subsidy",
        "name": "Karnataka Self Employment Subsidy Scheme",
        "level": "state",
        "state": "Karnataka",
        "category": "Finance",
        "eligibility": "Unemployed youth planning self-employment units.",
        "benefits": "Capital subsidy on project cost for eligible beneficiaries.",
        "apply_link": "https://www.kviconline.gov.in"
    },
    {
        "id": "ka_fin_artisan_credit_card",
        "name": "Artisan Credit Card Scheme",
        "level": "state",
        "state": "Karnataka",
        "category": "Finance",
        "eligibility": "Traditional artisans and craftsmen.",
        "benefits": "Working capital credit facility for artisan activities.",
        "apply_link": "https://services.karnataka.gov.in/artisan-credit"
    },

    # Central (3)
    {
        "id": "cen_fin_mudra",
        "name": "Pradhan Mantri MUDRA Yojana",
        "level": "central",
        "state": "India",
        "category": "Finance",
        "eligibility": "Non-farm small/micro enterprises and individuals.",
        "benefits": "Loans up to ₹10 lakh under Shishu, Kishor and Tarun categories.",
        "apply_link": "https://www.mudra.org.in"
    },
    {
        "id": "cen_fin_standup_india",
        "name": "Stand-Up India Scheme",
        "level": "central",
        "state": "India",
        "category": "Finance",
        "eligibility": "SC/ST and women entrepreneurs.",
        "benefits": "Bank loans between ₹10 lakh and ₹1 crore for greenfield enterprises.",
        "apply_link": "https://www.standupmitra.in"
    },
    {
        "id": "cen_fin_jan_dhan",
        "name": "Pradhan Mantri Jan Dhan Yojana",
        "level": "central",
        "state": "India",
        "category": "Finance",
        "eligibility": "Unbanked individuals above 10 years of age.",
        "benefits": "Zero-balance savings account, RuPay card and insurance cover.",
        "apply_link": "https://pmjdy.gov.in"
    },

    # =========================
    # 4. FOOD (10)
    # =========================

    # Karnataka (7)
    {
        "id": "ka_food_anna_bhagya",
        "name": "Anna Bhagya Free Rice Scheme",
        "level": "state",
        "state": "Karnataka",
        "category": "Food",
        "eligibility": "BPL and priority household ration card holders in Karnataka.",
        "benefits": "Free rice per person per month through PDS.",
        "apply_link": "https://ahara.kar.nic.in"
    },
    {
        "id": "ka_food_midday_meal_plus",
        "name": "Enhanced Mid-Day Meal Programme",
        "level": "state",
        "state": "Karnataka",
        "category": "Food",
        "eligibility": "Children enrolled in government and aided schools.",
        "benefits": "Nutritious cooked meals on all school working days.",
        "apply_link": "https://schooleducation.kar.nic.in"
    },
    {
        "id": "ka_food_maternal_nutrition",
        "name": "Maternal Nutrition Support Scheme",
        "level": "state",
        "state": "Karnataka",
        "category": "Food",
        "eligibility": "Pregnant and lactating women registered at Anganwadis.",
        "benefits": "Take-home rations and nutrition kits.",
        "apply_link": "https://dwcd.karnataka.gov.in"
    },
    {
        "id": "ka_food_tribal_nutrition_mission",
        "name": "Tribal Nutrition Mission",
        "level": "state",
        "state": "Karnataka",
        "category": "Food",
        "eligibility": "Tribal households in notified tribal hamlets.",
        "benefits": "Nutrition baskets and health check-ups.",
        "apply_link": "https://services.karnataka.gov.in/tribal-nutrition"
    },
    {
        "id": "ka_food_urban_poor_food_security",
        "name": "Urban Poor Food Security Scheme",
        "level": "state",
        "state": "Karnataka",
        "category": "Food",
        "eligibility": "Urban poor with BPL or Antyodaya ration cards.",
        "benefits": "Subsidized food grains and pulses through fair price shops.",
        "apply_link": "https://ahara.kar.nic.in"
    },
    {
        "id": "ka_food_anganwadi_supplementary",
        "name": "Anganwadi Supplementary Nutrition",
        "level": "state",
        "state": "Karnataka",
        "category": "Food",
        "eligibility": "Children 0–6 years registered at Anganwadi centres.",
        "benefits": "Hot cooked meals and take-home rations.",
        "apply_link": "https://dwcd.karnataka.gov.in"
    },
    {
        "id": "ka_food_migrant_worker_support",
        "name": "Migrant Worker Food Support Scheme",
        "level": "state",
        "state": "Karnataka",
        "category": "Food",
        "eligibility": "Registered migrant workers in urban areas.",
        "benefits": "Periodic dry ration kits during distress situations.",
        "apply_link": "https://labour.karnataka.gov.in"
    },

    # Central (3)
    {
        "id": "cen_food_pmgkay",
        "name": "Pradhan Mantri Garib Kalyan Anna Yojana",
        "level": "central",
        "state": "India",
        "category": "Food",
        "eligibility": "NFSA ration card holders.",
        "benefits": "Free foodgrains per person per month in addition to NFSA entitlement.",
        "apply_link": "https://nfsa.gov.in"
    },
    {
        "id": "cen_food_icds",
        "name": "Integrated Child Development Services Nutrition",
        "level": "central",
        "state": "India",
        "category": "Food",
        "eligibility": "Children 0–6 years, pregnant and lactating women.",
        "benefits": "Supplementary nutrition through Anganwadi centres.",
        "apply_link": "https://wcd.nic.in"
    },
    {
        "id": "cen_food_poshan_abhiyaan",
        "name": "POSHAN Abhiyaan",
        "level": "central",
        "state": "India",
        "category": "Food",
        "eligibility": "Women and children in high malnutrition districts.",
        "benefits": "Convergence actions to improve nutritional outcomes.",
        "apply_link": "https://poshanabhiyaan.gov.in"
    },

    # =========================
    # 5. HEALTH (10)
    # =========================

    # Karnataka (7)
    {
        "id": "ka_health_arogya_bhagya",
        "name": "Arogya Bhagya Health Cover",
        "level": "state",
        "state": "Karnataka",
        "category": "Health",
        "eligibility": "Eligible citizens enrolled under state health insurance.",
        "benefits": "Cashless treatment in empanelled hospitals for listed procedures.",
        "apply_link": "https://arogya.karnataka.gov.in"
    },
    {
        "id": "ka_health_yeshasvini",
        "name": "Yeshasvini Cooperative Health Scheme",
        "level": "state",
        "state": "Karnataka",
        "category": "Health",
        "eligibility": "Members of cooperative societies and their families.",
        "benefits": "Subsidized surgeries and hospitalization benefits.",
        "apply_link": "https://yeshasvini.karnataka.gov.in"
    },
    {
        "id": "ka_health_maternal_suraksha",
        "name": "Maternal Health Suraksha Scheme",
        "level": "state",
        "state": "Karnataka",
        "category": "Health",
        "eligibility": "Pregnant women registered at government health facilities.",
        "benefits": "Free antenatal care, institutional delivery and incentives.",
        "apply_link": "https://karunadu.karnataka.gov.in/hfw"
    },
    {
        "id": "ka_health_ncd_screening",
        "name": "Non-Communicable Disease Screening Programme",
        "level": "state",
        "state": "Karnataka",
        "category": "Health",
        "eligibility": "Adults above 30 years visiting PHCs and health camps.",
        "benefits": "Screening and referral for diabetes, hypertension and cancer.",
        "apply_link": "https://karunadu.karnataka.gov.in/hfw"
    },
    {
        "id": "ka_health_mental_health_helpline",
        "name": "Mental Health Support Helpline",
        "level": "state",
        "state": "Karnataka",
        "category": "Health",
        "eligibility": "Residents of Karnataka seeking mental health counseling.",
        "benefits": "24x7 toll-free helpline and tele-counselling services.",
        "apply_link": "https://karunadu.karnataka.gov.in/hfw"
    },
    {
        "id": "ka_health_rural_telemedicine",
        "name": "Rural Telemedicine Programme",
        "level": "state",
        "state": "Karnataka",
        "category": "Health",
        "eligibility": "Residents of rural areas using government telemedicine centres.",
        "benefits": "Online doctor consultation and e-prescriptions.",
        "apply_link": "https://karunadu.karnataka.gov.in/hfw"
    },
    {
        "id": "ka_health_free_dialysis",
        "name": "Free Dialysis Support Scheme",
        "level": "state",
        "state": "Karnataka",
        "category": "Health",
        "eligibility": "Poor kidney patients registered with government hospitals.",
        "benefits": "Free or subsidized dialysis sessions.",
        "apply_link": "https://karunadu.karnataka.gov.in/hfw"
    },

    # Central (3)
    {
        "id": "cen_health_pmjay",
        "name": "Ayushman Bharat - PM-JAY",
        "level": "central",
        "state": "India",
        "category": "Health",
        "eligibility": "Poor and vulnerable families identified as per SECC data.",
        "benefits": "Health cover up to ₹5 lakh per family per year for secondary and tertiary care.",
        "apply_link": "https://pmjay.gov.in"
    },
    {
        "id": "cen_health_janani_suraksha",
        "name": "Janani Suraksha Yojana",
        "level": "central",
        "state": "India",
        "category": "Health",
        "eligibility": "Pregnant women below poverty line or from SC/ST households.",
        "benefits": "Cash assistance for institutional delivery.",
        "apply_link": "https://nhm.gov.in"
    },
    {
        "id": "cen_health_national_dialysis",
        "name": "National Dialysis Programme",
        "level": "central",
        "state": "India",
        "category": "Health",
        "eligibility": "Chronic kidney disease patients in public hospitals.",
        "benefits": "Free dialysis services at district hospitals.",
        "apply_link": "https://nhm.gov.in"
    },

    # =========================
    # 6. POWER & ENERGY (10)
    # =========================

    # Karnataka (7)
    {
        "id": "ka_energy_rooftop_solar",
        "name": "Rooftop Solar Subsidy Scheme",
        "level": "state",
        "state": "Karnataka",
        "category": "Power & Energy",
        "eligibility": "Households and institutions installing rooftop solar.",
        "benefits": "Capital subsidy on rooftop solar installation.",
        "apply_link": "https://kredl.karnataka.gov.in"
    },
    {
        "id": "ka_energy_farm_pump_solarization",
        "name": "Farmer Pump-Set Solarization Scheme",
        "level": "state",
        "state": "Karnataka",
        "category": "Power & Energy",
        "eligibility": "Farmers with existing irrigation pump-sets.",
        "benefits": "Subsidy to convert grid-powered pumps to solar pumps.",
        "apply_link": "https://kredl.karnataka.gov.in"
    },
    {
        "id": "ka_energy_rural_electrification_support",
        "name": "Rural Household Electrification Support",
        "level": "state",
        "state": "Karnataka",
        "category": "Power & Energy",
        "eligibility": "Unelectrified households in rural Karnataka.",
        "benefits": "New electric connections at minimal cost.",
        "apply_link": "https://bescom.karnataka.gov.in"
    },
    {
        "id": "ka_energy_appliance_subsidy",
        "name": "Energy Efficient Appliance Subsidy",
        "level": "state",
        "state": "Karnataka",
        "category": "Power & Energy",
        "eligibility": "Domestic consumers and MSMEs.",
        "benefits": "Incentive for star-rated appliances to reduce power consumption.",
        "apply_link": "https://kredl.karnataka.gov.in"
    },
    {
        "id": "ka_energy_ev_charging_infra",
        "name": "EV Charging Infrastructure Support",
        "level": "state",
        "state": "Karnataka",
        "category": "Power & Energy",
        "eligibility": "Private and public entities setting up EV charging stations.",
        "benefits": "Capital subsidy and facilitation support.",
        "apply_link": "https://transport.karnataka.gov.in"
    },
    {
        "id": "ka_energy_solar_irrigation_pilot",
        "name": "Solar Irrigation Pilot Programme",
        "level": "state",
        "state": "Karnataka",
        "category": "Power & Energy",
        "eligibility": "Farmers in selected pilot taluks.",
        "benefits": "Support for community solar irrigation systems.",
        "apply_link": "https://kredl.karnataka.gov.in"
    },
    {
        "id": "ka_energy_msme_energy_audit",
        "name": "MSME Energy Audit Support Scheme",
        "level": "state",
        "state": "Karnataka",
        "category": "Power & Energy",
        "eligibility": "Registered MSME units.",
        "benefits": "Subsidy for energy audits and efficiency improvements.",
        "apply_link": "https://msmedept.karnataka.gov.in"
    },

    # Central (3)
    {
        "id": "cen_energy_pm_kusum",
        "name": "PM-KUSUM Solar Pump Scheme",
        "level": "central",
        "state": "India",
        "category": "Power & Energy",
        "eligibility": "Farmers and cooperatives installing solar pumps or plants.",
        "benefits": "Subsidy for solar pumps and decentralized solar power plants.",
        "apply_link": "https://mnre.gov.in"
    },
    {
        "id": "cen_energy_saubhagya",
        "name": "Saubhagya Household Electrification",
        "level": "central",
        "state": "India",
        "category": "Power & Energy",
        "eligibility": "Unelectrified rural and urban households.",
        "benefits": "Free electricity connections to poor households.",
        "apply_link": "https://saubhagya.gov.in"
    },
    {
        "id": "cen_energy_fame_india",
        "name": "FAME India Scheme",
        "level": "central",
        "state": "India",
        "category": "Power & Energy",
        "eligibility": "Individuals and entities purchasing approved EVs.",
        "benefits": "Demand incentive on electric vehicles and charging infrastructure.",
        "apply_link": "https://heavyindustries.gov.in"
    },

    # =========================
    # 7. LABOUR & EMPLOYMENT (10)
    # =========================

    # Karnataka (7)
    {
        "id": "ka_labour_skill_connect",
        "name": "Karnataka Skill Connect Programme",
        "level": "state",
        "state": "Karnataka",
        "category": "Labour & Employment",
        "eligibility": "Job seekers registering on state skill portal.",
        "benefits": "Training, job matching and placement assistance.",
        "apply_link": "https://skillconnect.karnataka.gov.in"
    },
    {
        "id": "ka_labour_cm_kaushalya",
        "name": "CM Kaushalya Yojana",
        "level": "state",
        "state": "Karnataka",
        "category": "Labour & Employment",
        "eligibility": "Youth between specified age group seeking skill training.",
        "benefits": "Free skill development courses with certification.",
        "apply_link": "https://skillconnect.karnataka.gov.in"
    },
    {
        "id": "ka_labour_bocw_welfare",
        "name": "Building & Other Construction Workers Welfare",
        "level": "state",
        "state": "Karnataka",
        "category": "Labour & Employment",
        "eligibility": "Registered construction workers in Karnataka.",
        "benefits": "Financial assistance, pensions, education aid and insurance.",
        "apply_link": "https://bocw.karnataka.gov.in"
    },
    {
        "id": "ka_labour_gig_worker_pilot",
        "name": "Gig Worker Social Security Pilot",
        "level": "state",
        "state": "Karnataka",
        "category": "Labour & Employment",
        "eligibility": "App-based gig workers registered in pilot districts.",
        "benefits": "Insurance and welfare benefits on co-contribution basis.",
        "apply_link": "https://labour.karnataka.gov.in"
    },
    {
        "id": "ka_labour_apprenticeship_promotion",
        "name": "State Apprenticeship Promotion Scheme",
        "level": "state",
        "state": "Karnataka",
        "category": "Labour & Employment",
        "eligibility": "Youth and industries registered under apprenticeship portal.",
        "benefits": "Stipend support and incentive for engaging apprentices.",
        "apply_link": "https://apprenticeshipindia.gov.in"
    },
    {
        "id": "ka_labour_women_shg_livelihoods",
        "name": "Women SHG Livelihood Promotion",
        "level": "state",
        "state": "Karnataka",
        "category": "Labour & Employment",
        "eligibility": "Women self-help group members.",
        "benefits": "Skill training, tool kits and market linkage for SHG enterprises.",
        "apply_link": "https://ksrlm.karnataka.gov.in"
    },
    {
        "id": "ka_labour_rural_employment_plus",
        "name": "Rural Employment Guarantee Plus",
        "level": "state",
        "state": "Karnataka",
        "category": "Labour & Employment",
        "eligibility": "Rural households willing to do unskilled manual work.",
        "benefits": "Additional employment days on top of central MGNREGA in selected areas.",
        "apply_link": "https://rdpr.karnataka.gov.in"
    },

    # Central (3)
    {
        "id": "cen_labour_mgnrega",
        "name": "Mahatma Gandhi NREGS",
        "level": "central",
        "state": "India",
        "category": "Labour & Employment",
        "eligibility": "Rural households willing to do unskilled manual work.",
        "benefits": "Guarantee of 100 days of wage employment per year.",
        "apply_link": "https://nrega.nic.in"
    },
    {
        "id": "cen_labour_pmkvY",
        "name": "Pradhan Mantri Kaushal Vikas Yojana",
        "level": "central",
        "state": "India",
        "category": "Labour & Employment",
        "eligibility": "Indian youth seeking short-term skill training.",
        "benefits": "Free skill training and assessment with certification.",
        "apply_link": "https://www.pmkvyofficial.org"
    },
    {
        "id": "cen_labour_naps",
        "name": "National Apprenticeship Promotion Scheme",
        "level": "central",
        "state": "India",
        "category": "Labour & Employment",
        "eligibility": "Establishments and apprentices registered on apprenticeship portal.",
        "benefits": "Sharing of stipend and basic training cost.",
        "apply_link": "https://apprenticeshipindia.gov.in"
    },
]


def main():
    col = db.collection("schemes")

    for scheme in SCHEMES:
        doc_id = scheme["id"]
        col.document(doc_id).set(scheme)
        print(f"✅ Upserted scheme: {doc_id}")

    print(f"🎉 Done. Seeded {len(SCHEMES)} schemes into Firestore.")


if __name__ == "__main__":
    main()
