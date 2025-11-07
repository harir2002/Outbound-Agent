# Outbound-Agent
# Outbound Call Demo - Streamlit Version

A Streamlit-based web application for automated outbound calling using Twilio API. This application replicates the exact look and functionality of the React version.

## Features

- 🌍 **Country Code Selection** - Support for 12+ countries
- 📞 **Phone Number Management** - Add and remove numbers from calling list
- 🎵 **Text-to-Speech** - Automated voice messages via Twilio
- 🎨 **Custom Theme** - Black/Red/White color scheme (matching React app)
- 📊 **Real-time Progress** - Live call status updates

## Installation

1. **Navigate to the streamlit folder**
   ```bash
   cd streamlit
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Twilio credentials**
   - Update the `.env` file with your Twilio credentials:
   ```
   TWILIO_ACCOUNT_SID=your_account_sid_here
   TWILIO_AUTH_TOKEN=your_auth_token_here
   TWILIO_PHONE_NUMBER=your_twilio_phone_number_here
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open in browser**
   - The app will automatically open at `http://localhost:8501`

## Usage

### 1. Add Phone Numbers
- Select country code from dropdown (default: India +91)
- Enter 10-digit phone number
- Click "Add to List" to add numbers

### 2. Review Message
- Edit the default banking reminder message
- Message will be converted to speech during calls

### 3. Send Calls
- Click "Send All Reminders" to initiate calls
- Monitor real-time progress
- View results after completion

## Twilio Setup

### Get Twilio Credentials:
1. Sign up at [Twilio.com](https://www.twilio.com/)
2. Go to [Twilio Console](https://console.twilio.com/)
3. Copy your Account SID and Auth Token
4. Purchase a phone number with Voice capabilities

### Pricing:
- **Outbound calls to India**: ~$0.012 per minute
- **Phone number rental**: ~$1/month

## File Structure

```
streamlit/
├── app.py              # Main Streamlit application
├── .env                # Environment variables (Twilio credentials)
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Color Scheme (Matching React App)

- **Primary Color**: #000000 (Black)
- **Secondary Color**: #e7000b (Red)
- **Text Color**: #ffffff (White)

## Troubleshooting

### Common Issues:

1. **"Twilio Connection Failed"**
   - Check your Account SID and Auth Token
   - Ensure credentials are correct in `.env` file

2. **"Call Failed - Unverified Number"**
   - For trial accounts, verify numbers in Twilio Console
   - Or upgrade to paid account for unrestricted calling

3. **"Module not found"**
   - Run `pip install -r requirements.txt`
   - Ensure you're in the streamlit directory

## Support

For issues or questions:
- Check Twilio documentation: [docs.twilio.com](https://www.twilio.com/docs)
- Streamlit documentation: [docs.streamlit.io](https://docs.streamlit.io)

---

**Built with ❤️ using Streamlit and Twilio**
