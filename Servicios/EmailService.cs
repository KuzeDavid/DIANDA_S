using SendGrid;
using SendGrid.Helpers.Mail;
using System;
using System.Threading.Tasks;

public class EmailService
{
    private readonly string _sendGridApiKey;

    public EmailService(string sendGridApiKey)
    {
        _sendGridApiKey = sendGridApiKey;
    }

    public async Task SendEmailAsync(string toEmail, string subject, string body)
    {
        var client = new SendGridClient(_sendGridApiKey);
        var from = new EmailAddress("helpdianda@gmail.com", "DIANDA");
        var to = new EmailAddress(toEmail);
        var msg = MailHelper.CreateSingleEmail(from, to, subject, body, body);

        try
        {
            var response = await client.SendEmailAsync(msg);
            Console.WriteLine($"Email sent (StatusCode: {response.StatusCode})");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error sending email: {ex.Message}");
            throw;
        }
    }
}
