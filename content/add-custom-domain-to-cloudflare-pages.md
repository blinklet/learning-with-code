title: Set up a Custom Domain for your Static Web Site on Cloudflare Pages
slug: add-custom-domain-to-cloudflare-pages
summary: Configure Cloudflare Pages to use a custom domain name, instead of the domain name *pages.dev* when it serves your static web site.
date: 2022-11-12
modified: 2022-11-12
category: Blogging
status: published

This post describes how to configure Cloudflare Pages to use a custom domain name, instead of the domain *pages.dev* when it serves your static web site. 

I purchase and manage my domains using [hover.com](https://www.hover.com). Hover offers an easy-to-use domain forwarding service. However, after the user is forwarded from my Hover-managed domain to Cloudflare Pages, the URL displayed by the browser changes to the Cloudflare URL. I want my URL, *learningwithcode.com* to remain visible on the browser. So, I will use the relatively more complex method of modifying DNS information so my custom domain name resolves directly to my site on Cloudflare Pages.

Cloudflare wrote a good document that tells you [how to modify your domain provider's and Cloudflare's DNS information](https://developers.cloudflare.com/dns/zone-setups/full-setup/setup/) so that a URL managed by another provider will point to a Cloudflare Pages site. The procedure is summarized below:

1. Temporarily [disable DNSSEC](https://developers.cloudflare.com/dns/zone-setups/full-setup/setup/#before-you-begin) on hover.com, or at your domain registrar. Cloudflare offers links to provider-specific instructions for disabling DNSSEC, [including one for hover.com](https://help.hover.com/hc/en-us/articles/217281647-Understanding-and-managing-DNSSEC).
2. [Add your domain](https://developers.cloudflare.com/fundamentals/get-started/setup/add-site/#step-1--add-site-in-cloudflare) in the Cloudflare Dashboard.
3. [Update your nameservers on hover.com](https://help.hover.com/hc/en-us/articles/217282477--Changing-your-domain-nameservers#:~:text=On%20the%20overview%20page%2C%20navigate%20to%20nameservers%20on,24-48%20hours%20for%20the%20change%20to%20be%20complete.),, or at your domain registrar, with the [CLoudflare nameserver information](https://developers.cloudflare.com/dns/zone-setups/full-setup/setup/#update-your-nameservers).
4. [Set up your SSL certificate](https://developers.cloudflare.com/ssl/get-started/) at Cloudflare Pages
5. [Re-enable DNSSEC on hover.com](https://help.hover.com/hc/en-us/articles/217281647-DNSSEC-services#:~:text=How%20to%20setup%20DNSSEC%3F%201%20Sign%20in%20to,your%20DNS%20hosting%20provider%20and%20click%20Add%20record.), or at your domain registrar.
6. Wait up to twenty four hours for nameserver changes to propagate across the Internet

## Temporarily disable DNSSEC on your domain

First, you need to disable [DNSSEC](https://www.icann.org/resources/pages/dnssec-what-is-it-why-important-2019-03-05-en) for your domain so you can change its configuration.

In my case, [I disabled DNSSEC on my domain at hover.com](https://help.hover.com/hc/en-us/articles/217281647-Understanding-and-managing-DNSSEC#h_f2d54352-35c2-4e7b-919b-60235407fea2) using the following steps:

* I signed into my [Hover control panel](https://hover.com/signin) 
* In the list of domains, I clicked on the domain I wish to configure, *learningwithcode.com*.
* I clicked on the *Advanced* tab on the page. In my case, DNSSEC is not yet configured because my domain is not configured yet.
  * If it was configured, I would have clicked *Edit* from the DNSSEC section for current settings.
  * I would have clicked *Clear Fields* to remove the DNSSEC.
  * I would have clicked *Save*.

## Add your domain to Cloudflare

Add your domain to Cloudflare's free plan level.  

* I logged into my [Cloudflare dashboard](https://dash.cloudflare.com/login).
* In the top navigation bar, I clicked *Add site*.
* I entered my website’s root domain, *learningwithcode.com*, and then clicked *Add Site*.
* Select your [plan level](https://www.cloudflare.com/plans/#compare-features). I chose the Free plan level. Click *Continue*.
* Review your DNS records. The records show up under the  *DNS* --> *Records* menu item. Cloudflare assigned your domain [two nameservers](https://developers.cloudflare.com/dns/zone-setups/full-setup/setup/#update-your-nameservers). You may have to scroll down a bit to see this information.
*  Make a note of the *Cloudflare nameserver* information so you can configure it at your domain registrar. 

## Update your domain's records in your registrar's dashboard

Add the Cloudflare [nameservers to the domain records](https://help.hover.com/hc/en-us/articles/217282477--Changing-your-domain-nameservers#:~:text=Adjusting%20nameservers%20for%20a%20single%20domain%201%20Sign,Save%20nameservers%20to%20push%20through%20the%20changes.%20) at your registrar. In my case, my registrar is *hover.com* so I performed the following steps:

* I signed into my [Hover control panel](https://hover.com/signin).
* In the list of domains, I clicked on the domain I wanted to configure, *learningwithcode.com*.
* On the domain's *Overview* page, I went to nameservers on the left-hand side of the page and selected *Edit*.
* I entered the nameserver information from Cloudflare Pages in the pop-up window.
* I clicked on *Save Nameservers*


## Set up an SSL Certificate for your Cloudflare Pages site

I [use *Universal SSL* for my domain at Cloudflare](https://developers.cloudflare.com/ssl/edge-certificates/universal-ssl/enable-universal-ssl/). Cloudflare manages the SSL certificates for my domain as long as it is hosted on Cloudflare pages.

My web site is hosted by Cloudflare Pages so I automatically get Univeral SSL enabled. I don't have to change anything.

## Re-enable DNSSEC on your domain

First, get the information you need to set up DNSSEC at hover.com, or at your domain registrar:

* I logged into my [Cloudflare dashboard](https://dash.cloudflare.com/login).
* I selected my domain, *learningwithcode.com*
* I went to *DNS* > *Settings*.
* For *DNSSEC*, I clicked *Enable DNSSEC*.
* In the *Enable DNSSEC* dialog box, I took note of the values to I need to re-enable DNSSEC at hover.com. Keep this page open so you can access the configurations when you need them

Then, go to hover.com in a new browser tab, or your domain registrar, and re-enable DNSSEC:

* I signed into my [Hover control panel](https://hover.com/signin) 
* In the list of domains, I clicked on the domain I wish to configure, *learningwithcode.com*.
* In the domain's *Advanced* page, I clicked on *Add a DNSSEC record*
* I added the settings to the required fields. In my case, Hover asked for the *Key Tag*, the *Algorithm*, the *Digest Algorith*, and the *Digest*.

## Enable e-mail security

If you plan to use your domain as part of an e-mail address, you may want to enable e-mail security for your custom domain. This helps you detect when scammers spoof your domain name in their e-mail addresses. I actually had this problem with another domain I used for e-mail and it was a real pain.

In the Cloudflare Dashboard menu for your domain, click on *Email* --> *DMARC Management*.

## Set up custom domain for Cloudflare Pages site

To add a [custom domain for your Cloudflare Pages site](https://developers.cloudflare.com/pages/platform/custom-domains/):

* I logged into my [Cloudflare dashboard](https://dash.cloudflare.com/login).
* I selected *Workers & Pages* and selected my pages site, 
* Select your *Pages project* --> *Custom domains*.
* Select *Set up a custom domain*.
* I entered "learningwithcode.com" as the domain name to serve my Cloudflare Pages site and selected *Continue*. Then *Activate domain* in the next page.

## Conclusion

Now, anyone who enters the URL *https://learningwithcode.com* will be directed to my static web site hosted on Cloudflare Pages. Cloudflare creates a wildcard DNS record so the domain *www.learningwithcode.com* should also work.


