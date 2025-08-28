# agent/nodes/retriever.py
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from agent.config import OPENROUTER_API_KEY
import os

embedding = HuggingFaceEmbeddings(model_name="thenlper/gte-large")

# Expanded knowledge base with comprehensive documentation for the four original categories
CATEGORY_DOCS = {
    "billing": [
        # Payment Processing
        Document(page_content="Billing occurs monthly on the same date you first subscribed. Invoices are automatically sent via email 3 days before the charge date."),
        Document(page_content="We accept Visa, MasterCard, American Express, and PayPal for payments. Cryptocurrency payments are available for enterprise accounts."),
        Document(page_content="You can update your payment method under Account Settings > Billing. Changes take effect immediately for future charges."),
        Document(page_content="Failed payments will automatically retry after 3 days, then 7 days, then 14 days before account suspension."),
        Document(page_content="Payment failures result in email notifications to both primary and billing contact emails if different."),
        
        # Refunds and Credits
        Document(page_content="Refunds can only be issued with supervisor approval within 30 days of payment. Partial refunds are available for unused service time."),
        Document(page_content="Service credits are automatically applied for documented downtime exceeding 99.5% uptime SLA commitment."),
        Document(page_content="Pro-rated refunds are available when downgrading plans mid-cycle. The difference is credited to your account."),
        Document(page_content="Subscription cancellation takes effect at the end of the current billing period. No partial refunds for cancellations."),
        
        # Pricing and Plans
        Document(page_content="Discount codes must be applied before checkout is completed. Codes cannot be applied retroactively to existing subscriptions."),
        Document(page_content="Student discounts of 50% are available with valid .edu email verification. Academic institution bulk pricing available."),
        Document(page_content="Annual subscriptions receive 2 months free compared to monthly billing. Enterprise plans include custom pricing."),
        Document(page_content="Plan upgrades are immediate with pro-rated billing. Downgrades take effect at the next billing cycle."),
        
        # Account Management
        Document(page_content="Billing statements can be downloaded as PDF from your account dashboard. Statements include detailed usage metrics."),
        Document(page_content="Tax invoices are generated automatically for business accounts. VAT/GST calculations are applied based on billing address."),
        Document(page_content="Account managers are assigned to enterprise customers for billing support. Quarterly business reviews included in enterprise plans."),
        Document(page_content="Self-service billing options include payment method updates, invoice downloads, and subscription plan changes through the dashboard.")
    ],
    
    "technical": [
        # Application Issues
        Document(page_content="For technical issues, first try clearing your app cache or reinstalling the application. This resolves 80% of reported issues."),
        Document(page_content="Version 2.1.0 fixed most known bugs from 2.0, including memory leaks and sync failures. Always update to the latest version."),
        Document(page_content="Mobile login failures are often resolved by updating the app, clearing cache, or checking device date/time settings."),
        Document(page_content="If the system crashes, check the log file in your install directory at /logs/error.log for specific error messages."),
        Document(page_content="Database sync issues can be resolved by going to Settings > Sync > Force Sync. This may take 5-10 minutes for large datasets."),
        
        # Platform Compatibility
        Document(page_content="Some features like bulk export and advanced analytics are only available on the desktop version of the app."),
        Document(page_content="Minimum system requirements: Windows 10, macOS 10.14, or Linux Ubuntu 18.04+. 4GB RAM and 2GB storage required."),
        Document(page_content="Browser compatibility: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+. Internet Explorer is not supported."),
        Document(page_content="Mobile apps require iOS 13+ or Android 8.0+. Tablet optimization available for iPad and Android tablets 10+ inches."),
        
        # Performance and Optimization
        Document(page_content="Slow performance is often caused by large file attachments. Consider using cloud storage links instead of direct uploads."),
        Document(page_content="API rate limits are 1000 requests per hour for standard accounts, 5000 for premium accounts. Enterprise has custom limits."),
        Document(page_content="Offline mode stores up to 30 days of data locally. Sync automatically resumes when internet connection is restored."),
        Document(page_content="Network connectivity issues can be diagnosed using the built-in connection test in Settings > Diagnostics > Network Test."),
        
        # Integration Support
        Document(page_content="Third-party integrations support Zapier, Microsoft Power Automate, and direct API connections. Webhooks available for real-time updates."),
        Document(page_content="SSO integration supports SAML 2.0, OAuth 2.0, and LDAP. Azure AD and Google Workspace are pre-configured options."),
        Document(page_content="Data export formats include CSV, JSON, XML, and PDF. Bulk exports are processed within 24 hours and sent via email link."),
        Document(page_content="Backup and restore functionality available in Settings > Data Management. Automated backups run daily for premium accounts.")
    ],
    
    "security": [
        # Authentication and Access
        Document(page_content="Security protocols include mandatory 2FA and AES-256 encryption-at-rest for all user data. TLS 1.3 for data in transit."),
        Document(page_content="Do not share login credentials or recovery tokens with anyone. Each user should have their own account for audit trail purposes."),
        Document(page_content="All admin access is logged and reviewed weekly. Failed login attempts trigger automatic security alerts after 5 attempts."),
        Document(page_content="Session timeout is 8 hours for regular users, 4 hours for admin accounts. Sessions can be extended but require re-authentication."),
        Document(page_content="Account lockout occurs after 10 failed login attempts. Unlocking requires email verification or admin override."),
        
        # Data Protection and Compliance
        Document(page_content="We comply with GDPR, CCPA, and SOC 2 Type II standards. Annual security audits performed by third-party firms."),
        Document(page_content="Data retention policy: Active data indefinitely, deleted data purged after 90 days. Legal hold overrides standard retention."),
        Document(page_content="Personal data requests (access, deletion, portability) are processed within 30 days as required by privacy regulations."),
        Document(page_content="Data centers are ISO 27001 certified with 24/7 physical security, biometric access, and redundant power/cooling systems."),
        
        # Account Security
        Document(page_content="Security questions can be reset via the verified email address. Backup codes are provided for accounts with 2FA enabled."),
        Document(page_content="Password requirements: minimum 12 characters with uppercase, lowercase, numbers, and symbols. Dictionary words prohibited."),
        Document(page_content="Suspicious activity monitoring includes login location tracking, device fingerprinting, and behavioral analysis."),
        Document(page_content="Security incidents are reported to affected users within 72 hours. Incident response team available 24/7 for critical issues."),
        
        # Security Features
        Document(page_content="Bug bounty program rewards security researchers for responsible disclosure. Rewards range from $100 to $10,000."),
        Document(page_content="Regular penetration testing is performed quarterly. Vulnerability assessments include both automated and manual testing."),
        Document(page_content="IP whitelisting available for enterprise accounts. VPN access can be configured for secure remote connections."),
        Document(page_content="Audit logs are available for all user actions and can be exported for compliance purposes. Logs retained for 7 years.")
    ],
    
    "general": [
        # Support Information
        Document(page_content="We are always happy to help with account issues, preferences, feedback, or any questions about our service."),
        Document(page_content="Support hours are Monday–Friday, 9 AM to 6 PM PST. Emergency support available 24/7 for enterprise customers."),
        Document(page_content="Use our in-app chat to reach a support agent instantly during business hours. Average response time is under 2 minutes."),
        Document(page_content="You can access comprehensive tutorials and guides in the Help Center at help.ourcompany.com with video walkthroughs."),
        Document(page_content="Email support available at support@ourcompany.com with 24-hour response time guarantee for all inquiries."),
        
        # Team and Training
        Document(page_content="Our support team is trained to handle both product and account queries. Level 2 technical specialists available for complex issues."),
        Document(page_content="All support agents receive monthly training on new features and common issues. Customer satisfaction ratings averaged 4.8/5 last quarter."),
        Document(page_content="Escalation to product managers available for feature requests. Development roadmap is updated quarterly based on user feedback."),
        
        # Resources and Self-Help
        Document(page_content="Video tutorials cover basic setup, advanced features, and troubleshooting. New user onboarding includes guided product tours."),
        Document(page_content="Community forum allows users to share tips and solutions. Most active community members receive special recognition badges."),
        Document(page_content="Knowledge base includes searchable articles, FAQ sections, and step-by-step guides with screenshots for visual learners."),
        Document(page_content="Status page at status.ourcompany.com provides real-time service health updates and scheduled maintenance notifications."),
        
        # Communication Channels
        Document(page_content="Phone support available for premium customers at 1-800-SUPPORT. International toll-free numbers available in 12 countries."),
        Document(page_content="Social media support on Twitter @OurCompanyHelp and Facebook. Public issues are addressed within 4 hours during business days."),
        Document(page_content="Live webinars hosted monthly covering new features and best practices. Recordings available in the Help Center."),
        Document(page_content="User feedback is collected through in-app surveys, support interactions, and quarterly user research studies."),
        
        # Account and Profile Management  
        Document(page_content="Account profile can be updated in User Settings including name, email, phone, and profile picture. Changes sync across all devices."),
        Document(page_content="Team accounts support role-based permissions: Owner, Admin, Member, and Viewer. Custom roles available for enterprise plans."),
        Document(page_content="Data export includes all user-generated content, settings, and activity logs. Export processing takes 1-3 business days."),
        Document(page_content="Language settings support 15 languages including English, Spanish, French, German, Japanese, and Mandarin Chinese.")
    ]
}

# Create FAISS databases for each category
FAISS_DB = {
    cat: FAISS.from_documents(docs, embedding)
    for cat, docs in CATEGORY_DOCS.items()
}

def retrieve_context(state):
    """Retrieve relevant context documents based on ticket category and content"""
    category = state["category"].lower()
    query = f"{state['subject']} {state['description']}"
    
    # Get retriever for the category, fallback to general if category not found
    retriever = FAISS_DB.get(category, FAISS_DB["general"]).as_retriever(
        search_type="similarity", 
        k=3  # Increased from 2 to 3 for better context
    )
    
    results = retriever.invoke(query)
    context_docs = [doc.page_content for doc in results]
    
    # Also search general category for additional context if not already general
    if category != "general":
        general_retriever = FAISS_DB["general"].as_retriever(search_type="similarity", k=1)
        general_results = general_retriever.invoke(query)
        context_docs.extend([doc.page_content for doc in general_results])
    
    return {**state, "context": context_docs}