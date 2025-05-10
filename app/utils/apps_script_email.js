/**
 * Google Apps Script for sending emails via Gmail
 * 
 * This script creates a web app that receives POST requests and sends emails through Gmail.
 * Deploy as a web app and set access to "Anyone, even anonymous" for webhook access.
 */

function doPost(e) {
  try {
    // Parse the incoming JSON payload
    const payload = JSON.parse(e.postData.contents);
    
    // Extract email details
    const recipient = payload.recipient;
    const subject = payload.subject;
    const message = payload.message;
    const attachment = payload.attachment;
    
    // Validate required fields
    if (!recipient || !subject) {
      return ContentService.createTextOutput(
        JSON.stringify({ success: false, error: "Missing required fields" })
      ).setMimeType(ContentService.MimeType.JSON);
    }
    
    // If there's an attachment, process it
    let options = {};
    if (attachment) {
      // Decode the base64 data
      const decoded = Utilities.base64Decode(attachment.data);
      const blob = Utilities.newBlob(decoded, attachment.mimeType, attachment.filename);
      options = { attachments: [blob] };
    }
    
    // Send the email
    GmailApp.sendEmail(recipient, subject, message, options);
    
    // Return success response
    return ContentService.createTextOutput(
      JSON.stringify({ success: true, message: "Email sent successfully" })
    ).setMimeType(ContentService.MimeType.JSON);
    
  } catch (error) {
    // Return error response
    return ContentService.createTextOutput(
      JSON.stringify({ success: false, error: error.toString() })
    ).setMimeType(ContentService.MimeType.JSON);
  }
}

/**
 * Test function to ensure the script is working
 */
function testEmailSend() {
  // Replace with your email for testing
  const testEmail = Session.getActiveUser().getEmail();
  
  GmailApp.sendEmail(
    testEmail,
    "Test Email from Google Apps Script",
    "This is a test email sent from Google Apps Script."
  );
  
  Logger.log("Test email sent to: " + testEmail);
}

/**
 * Required for web app deployment
 */
function doGet() {
  return HtmlService.createHtmlOutput(
    "<h1>HRIM Wellness Email Service</h1><p>This is a webhook endpoint for sending emails. Please use POST requests.</p>"
  );
} 