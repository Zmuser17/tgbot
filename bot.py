from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
import logging
import json
import os
from datetime import datetime
import csv
import uuid

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation states
(
    GET_NAME, GET_EMAIL, GET_PHONE, GET_DOB, GET_COUNTRY, 
    GET_PASSPORT_NO, GET_PASSPORT_EXPIRY, GET_BIRTH_PLACE,
    GET_EDUCATION_LEVEL, GET_SCHOOL_NAME, GET_GRADUATION_YEAR, GET_FIELD_STUDY, GET_GPA,
    GET_DESIRED_LEVEL, GET_PREFERRED_FIELD, GET_RUSSIAN_LEVEL,
    GET_SERVICE_PACKAGE
) = range(17)

CSV_FILE = "scholarship_applications.csv"

def init_csv_file():
    """Initialize CSV file with headers if it doesn't exist."""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                'application_id', 'user_id', 'timestamp', 'name', 'email', 'phone', 
                'date_of_birth', 'country', 'passport_number', 'passport_expiry', 
                'birth_place', 'education_level', 'school_name', 'graduation_year',
                'field_study', 'gpa', 'desired_level', 'preferred_field', 
                'russian_level', 'service_package', 'price', 'status'
            ])
        print("CSV file created with headers")

def save_to_csv(application_data):
    """Save application data to CSV file."""
    try:
        # Generate unique application ID
        application_id = str(uuid.uuid4())[:8]
        application_data['application_id'] = application_id
        
        # Write to CSV
        with open(CSV_FILE, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                application_data.get('application_id', ''),
                application_data.get('user_id', ''),
                application_data.get('timestamp', ''),
                application_data.get('name', ''),
                application_data.get('email', ''),
                application_data.get('phone', ''),
                application_data.get('date_of_birth', ''),
                application_data.get('country', ''),
                application_data.get('passport_number', ''),
                application_data.get('passport_expiry', ''),
                application_data.get('birth_place', ''),
                application_data.get('education_level', ''),
                application_data.get('school_name', ''),
                application_data.get('graduation_year', ''),
                application_data.get('field_study', ''),
                application_data.get('gpa', ''),
                application_data.get('desired_level', ''),
                application_data.get('preferred_field', ''),
                application_data.get('russian_level', ''),
                application_data.get('service_package', ''),
                application_data.get('price', ''),
                application_data.get('status', '')
            ])
        
        print(f"Application {application_id} saved to CSV")
        return application_id
        
    except Exception as e:
        print(f"Error saving to CSV: {e}")
        return None

def find_application_by_user_id(user_id):
    """Find application by user ID in CSV file."""
    try:
        if os.path.exists(CSV_FILE):
            with open(CSV_FILE, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                applications = list(reader)
                for app in reversed(applications):  # Start from most recent
                    if app['user_id'] == str(user_id):
                        return app
        return None
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return None

# Initialize CSV file when bot starts
init_csv_file()

# ============================================================================
# BOT COMMAND FUNCTIONS
# ============================================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message when command /start is issued."""
    user = update.message.from_user
    await update.message.reply_text(
        f"🤖 *Welcome {user.first_name} to Russia Scholarship Service!*\n\n"
        "I will help you apply for the Russian Government Scholarship.\n\n"
        "📋 *Available Commands:*\n"
        "/apply - Start new application\n"
        "/status - Check your application status\n"
        "/help - Get help and instructions\n"
        "/cancel - Cancel current operation\n\n"
        "Click /apply to begin your scholarship journey! 🎓",
        parse_mode='Markdown'
    )

async def apply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the application process."""
    context.user_data.clear()
    
    await update.message.reply_text(
        "🤖 *Welcome to Russia Scholarship Service!*\n\n"
        "I will help you apply for the Russian Government Scholarship.\n\n"
        "Let's start with your personal information. This will take about 10-15 minutes.\n\n"
        "📝 *Please type your FULL NAME as it appears in your passport:*\n\n"
        "Type /cancel at any time to stop the application.",
        parse_mode='Markdown'
    )
    return GET_NAME

# ============================================================================
# SECTION 1: PERSONAL INFORMATION
# ============================================================================

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store name and ask for email."""
    name = update.message.text
    context.user_data['name'] = name
    context.user_data['timestamp'] = datetime.now().isoformat()
    
    await update.message.reply_text(
        f"✅ **Name recorded:** {name}\n\n"
        "Now, please provide your:\n"
        "📧 **EMAIL ADDRESS:**"
    )
    return GET_EMAIL

async def get_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store email and ask for phone."""
    email = update.message.text
    context.user_data['email'] = email
    
    await update.message.reply_text(
        f"✅ **Email recorded:** {email}\n\n"
        "📞 **PHONE NUMBER (with country code):**\n"
        "Example: +1234567890"
    )
    return GET_PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store phone and ask for date of birth."""
    phone = update.message.text
    context.user_data['phone'] = phone
    
    await update.message.reply_text(
        f"✅ **Phone recorded:** {phone}\n\n"
        "📅 **DATE OF BIRTH (DD/MM/YYYY):**\n"
        "Example: 15/05/2000"
    )
    return GET_DOB

async def get_dob(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store date of birth and ask for country."""
    dob = update.message.text
    context.user_data['date_of_birth'] = dob
    
    await update.message.reply_text(
        f"✅ **Date of birth recorded:** {dob}\n\n"
        "🌍 **COUNTRY OF CITIZENSHIP:**\n"
        "Example: Nigeria, India, Pakistan, etc."
    )
    return GET_COUNTRY

async def get_country(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store country and ask for passport number."""
    country = update.message.text
    context.user_data['country'] = country
    
    await update.message.reply_text(
        f"✅ **Country recorded:** {country}\n\n"
        "📔 **PASSPORT NUMBER:**\n"
        "Example: A12345678"
    )
    return GET_PASSPORT_NO

async def get_passport_no(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store passport number and ask for expiry date."""
    passport_no = update.message.text
    context.user_data['passport_number'] = passport_no
    
    await update.message.reply_text(
        f"✅ **Passport number recorded:** {passport_no}\n\n"
        "📅 **PASSPORT EXPIRY DATE (DD/MM/YYYY):**\n"
        "Example: 15/05/2030"
    )
    return GET_PASSPORT_EXPIRY

async def get_passport_expiry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store passport expiry and ask for birth place."""
    passport_expiry = update.message.text
    context.user_data['passport_expiry'] = passport_expiry
    
    await update.message.reply_text(
        f"✅ **Passport expiry recorded:** {passport_expiry}\n\n"
        "📍 **PLACE OF BIRTH (City, Country):**\n"
        "Example: Lagos, Nigeria"
    )
    return GET_BIRTH_PLACE

async def get_birth_place(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store birth place and move to education section."""
    birth_place = update.message.text
    context.user_data['birth_place'] = birth_place
    
    # Create education level keyboard
    keyboard = [
        ["High School Diploma", "Bachelor's Degree"],
        ["Master's Degree", "Other"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    
    await update.message.reply_text(
        f"✅ **Birth place recorded:** {birth_place}\n\n"
        "🎓 **Now let's talk about your education:**\n\n"
        "**What is your HIGHEST EDUCATION LEVEL?**\n"
        "Choose one from below:",
        reply_markup=reply_markup
    )
    return GET_EDUCATION_LEVEL

# ============================================================================
# SECTION 2: EDUCATION BACKGROUND
# ============================================================================

async def get_education_level(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store education level and ask for school name."""
    education_level = update.message.text
    context.user_data['education_level'] = education_level
    
    await update.message.reply_text(
        f"✅ **Education level recorded:** {education_level}\n\n"
        "🏫 **NAME OF SCHOOL/UNIVERSITY:**\n"
        "Example: University of Lagos",
        reply_markup=ReplyKeyboardRemove()
    )
    return GET_SCHOOL_NAME

async def get_school_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store school name and ask for graduation year."""
    school_name = update.message.text
    context.user_data['school_name'] = school_name
    
    await update.message.reply_text(
        f"✅ **School recorded:** {school_name}\n\n"
        "📅 **YEAR OF GRADUATION:**\n"
        "Example: 2023"
    )
    return GET_GRADUATION_YEAR

async def get_graduation_year(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store graduation year and ask for field of study."""
    graduation_year = update.message.text
    context.user_data['graduation_year'] = graduation_year
    
    await update.message.reply_text(
        f"✅ **Graduation year recorded:** {graduation_year}\n\n"
        "📚 **FIELD OF STUDY:**\n"
        "Example: Computer Science, Business Administration, Medicine"
    )
    return GET_FIELD_STUDY

async def get_field_study(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store field of study and ask for GPA."""
    field_study = update.message.text
    context.user_data['field_study'] = field_study
    
    await update.message.reply_text(
        f"✅ **Field of study recorded:** {field_study}\n\n"
        "📊 **GPA OR GRADES (Optional):**\n"
        "Example: 3.5/4.0 or 85%\n"
        "You can type 'Skip' if you prefer not to share"
    )
    return GET_GPA

async def get_gpa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store GPA and move to study preferences."""
    gpa = update.message.text
    if gpa.lower() != 'skip':
        context.user_data['gpa'] = gpa
    
    # Create desired level keyboard
    keyboard = [
        ["Bachelor's Degree", "Master's Degree"],
        ["PhD/Postgraduate", "Preparatory Course"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    
    await update.message.reply_text(
        "✅ **Education information complete!**\n\n"
        "📚 **What do you want to study in Russia?**\n\n"
        "**Choose your desired level:**",
        reply_markup=reply_markup
    )
    return GET_DESIRED_LEVEL

# ============================================================================
# SECTION 3: STUDY PREFERENCES
# ============================================================================

async def get_desired_level(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store desired level and ask for preferred field."""
    desired_level = update.message.text
    context.user_data['desired_level'] = desired_level
    
    # Create preferred field keyboard
    keyboard = [
        ["Medicine & Healthcare", "Engineering & Technology"],
        ["Business & Economics", "Computer Science & IT"],
        ["Arts & Humanities", "Science & Mathematics"],
        ["Other Field"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    
    await update.message.reply_text(
        f"✅ **Desired level recorded:** {desired_level}\n\n"
        "**Preferred Field:**\n"
        "Choose your field of interest:",
        reply_markup=reply_markup
    )
    return GET_PREFERRED_FIELD

async def get_preferred_field(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store preferred field and ask for Russian level."""
    preferred_field = update.message.text
    context.user_data['preferred_field'] = preferred_field
    
    # Create Russian level keyboard
    keyboard = [
        ["None", "Beginner"],
        ["Intermediate", "Advanced"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    
    await update.message.reply_text(
        f"✅ **Preferred field recorded:** {preferred_field}\n\n"
        "🇷🇺 **RUSSIAN LANGUAGE LEVEL:**\n"
        "Choose your current level:",
        reply_markup=reply_markup
    )
    return GET_RUSSIAN_LEVEL

async def get_russian_level(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store Russian level and move to service packages."""
    russian_level = update.message.text
    context.user_data['russian_level'] = russian_level
    
    # Create service package keyboard
    keyboard = [
        ["Basic Application Service - Form completion, Document review, Application submission"],
        ["Premium Full Service - Everything in Basic + Document preparation, University selection"],
        ["VIP Complete Package - Everything in Premium + Visa assistance, Accommodation help"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    
    await update.message.reply_text(
        f"✅ **Russian level recorded:** {russian_level}\n\n"
        "💼 **Almost done! Please choose your service package:**\n\n"
        "**Basic Application Service ($50)**\n"
        "• Form completion\n"
        "• Document review  \n"
        "• Application submission\n\n"
        "**Premium Full Service ($100)**  \n"
        "• Everything in Basic +\n"
        "• Document preparation help\n"
        "• University selection advice\n\n"
        "**VIP Complete Package ($200)**\n"
        "• Everything in Premium +\n"
        "• Visa assistance\n"
        "• Accommodation help\n\n"
        "Select your preferred option:",
        reply_markup=reply_markup
    )
    return GET_SERVICE_PACKAGE

# ============================================================================
# SECTION 5: SERVICE AGREEMENT & PAYMENT
# ============================================================================

async def get_service_package(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store service package and complete application."""
    service_package = update.message.text
    context.user_data['service_package'] = service_package
    context.user_data['status'] = "submitted"
    
    # Determine price based on service
    if "Basic" in service_package:
        price = "$50"
    elif "Premium" in service_package:
        price = "$100"
    else:
        price = "$200"
    
    context.user_data['price'] = price
    context.user_data['user_id'] = update.message.from_user.id
    context.user_data['timestamp'] = datetime.now().isoformat()
    
    # Save to CSV
    application_id = save_to_csv(context.user_data)
    
    # Send final confirmation
    if application_id:
        await update.message.reply_text(
            f"🎉 **APPLICATION SUBMITTED SUCCESSFULLY!** 🎉\n\n"
            f"📋 **Application ID:** {application_id}\n"
            f"👤 **Name:** {context.user_data['name']}\n"
            f"📧 **Email:** {context.user_data['email']}\n"
            f"📞 **Phone:** {context.user_data['phone']}\n"
            f"🎓 **Education:** {context.user_data['education_level']}\n"
            f"📚 **Desired Study:** {context.user_data['desired_level']} in {context.user_data['preferred_field']}\n"
            f"💼 **Service:** {context.user_data['service_package']}\n"
            f"💰 **Price:** {price}\n\n"
            "**📄 Next Steps - Document Collection:**\n"
            "Please prepare these documents:\n"
            "1. 📔 Passport scan (main page with photo)\n"
            "2. 🎓 Educational diplomas/certificates\n" 
            "3. 📊 Academic transcripts\n"
            "4. 📸 Passport-sized photo\n"
            "5. 🏥 Medical certificate (if available)\n\n"
            "We will contact you within 24 hours to collect your documents "
            "and complete the official application process.\n\n"
            "Use /status to check your application progress.\n"
            "Thank you for choosing our service! 🙏",
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        await update.message.reply_text(
            "❌ **Error saving application!** Please contact support.",
            reply_markup=ReplyKeyboardRemove()
        )
    
    # Clear conversation data
    context.user_data.clear()
    return ConversationHandler.END

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check application status."""
    user_id = update.message.from_user.id
    application = find_application_by_user_id(user_id)
    
    if application:
        status_msg = "✅ **Application Received**" if application.get('status') == 'submitted' else "⏳ **Processing**"
        
        await update.message.reply_text(
            f"📋 **YOUR APPLICATION STATUS**\n\n"
            f"🆔 **Application ID:** {application.get('application_id', 'N/A')}\n"
            f"👤 **Name:** {application.get('name', 'N/A')}\n"
            f"📧 **Email:** {application.get('email', 'N/A')}\n"
            f"📞 **Phone:** {application.get('phone', 'N/A')}\n"
            f"🌍 **Country:** {application.get('country', 'N/A')}\n"
            f"🎓 **Education:** {application.get('education_level', 'N/A')}\n"
            f"📚 **Desired:** {application.get('desired_level', 'N/A')} in {application.get('preferred_field', 'N/A')}\n"
            f"💼 **Service:** {application.get('service_package', 'N/A')}\n"
            f"💰 **Price:** {application.get('price', 'N/A')}\n"
            f"📅 **Submitted:** {application.get('timestamp', 'N/A')[:10]}\n\n"
            f"**Status:** {status_msg}\n\n"
            "We'll contact you soon to collect your documents!"
        )
    else:
        await update.message.reply_text(
            "❌ **No application found!**\n\n"
            "You haven't submitted an application yet.\n"
            "Use /apply to start your scholarship application."
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a help message."""
    await update.message.reply_text(
        "🆘 **HELP & INSTRUCTIONS**\n\n"
        "📋 **How to Apply:**\n"
        "1. Use /apply to start application\n"
        "2. Follow the step-by-step instructions\n"
        "3. Provide your information when asked\n"
        "4. Choose your service package\n"
        "5. Submit your application\n\n"
        "📊 **Check Status:**\n"
        "Use /status to see your application progress\n\n"
        "📄 **Documents Needed:**\n"
        "• Passport scan\n"
        "• Educational certificates\n"
        "• Academic transcripts\n"
        "• Passport photo\n"
        "• Medical certificate\n\n"
        "💼 **Service Packages:**\n"
        "• Basic - Form filling assistance ($50)\n"
        "• Premium - Full application help ($100)\n"
        "• VIP - Complete process handling ($200)\n\n"
        "❌ **Cancel:** Use /cancel to stop current application"
    )

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel the current conversation."""
    context.user_data.clear()
    await update.message.reply_text(
        "❌ Application cancelled.\n\n"
        "Your progress has been saved. You can start again with /apply anytime!",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

async def handle_unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle unknown commands and messages."""
    await update.message.reply_text(
        "🤔 I don't understand that command.\n\n"
        "Try one of these:\n"
        "/start - Welcome message\n"
        "/apply - Start application\n"
        "/status - Check status\n"
        "/help - Get help\n"
        "/cancel - Cancel operation"
    )

def main():
    """Start the bot."""
    # Read bot token from environment variable for security
    TOKEN = "8295648137:AAGl0VLcqCB8Rx6uOqaytL1SyEh3Ed5FFPI"  # Your actual token
    if not TOKEN:
        logger.error("Bot token is not set. Exiting.")
        raise SystemExit("Error: BOT_TOKEN environment variable not set. Set it and restart the bot.")
    
    # Create the Application
    
    application = Application.builder().token(TOKEN).build()
    
    # Add conversation handler for /apply command
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('apply', apply)],
        states={
            # Personal Information
            GET_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            GET_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_email)],
            GET_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
            GET_DOB: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_dob)],
            GET_COUNTRY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_country)],
            GET_PASSPORT_NO: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_passport_no)],
            GET_PASSPORT_EXPIRY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_passport_expiry)],
            GET_BIRTH_PLACE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_birth_place)],
            
            # Education Background
            GET_EDUCATION_LEVEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_education_level)],
            GET_SCHOOL_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_school_name)],
            GET_GRADUATION_YEAR: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_graduation_year)],
            GET_FIELD_STUDY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_field_study)],
            GET_GPA: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_gpa)],
            
            # Study Preferences
            GET_DESIRED_LEVEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_desired_level)],
            GET_PREFERRED_FIELD: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_preferred_field)],
            GET_RUSSIAN_LEVEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_russian_level)],
            
            # Service Package
            GET_SERVICE_PACKAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_service_package)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    
    # Add other command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(conv_handler)
    
    # Handle unknown commands and messages
    application.add_handler(MessageHandler(filters.ALL, handle_unknown))
    
    # Start the Bot
    print("Russia Scholarship Bot is starting...")
    print("Bot is running! Press Ctrl+C to stop.")
    application.run_polling()

if __name__ == '__main__':
    main()