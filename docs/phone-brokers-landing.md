---
published: false
---

# Phone checklist: brokers landing page (website PR #7)

Billy reviews the `/brokers` landing page on a phone in South Africa (Safari or Chrome), then stops. Publish waits for his own yes. This page is the tap path for [website pull request #7](https://github.com/billyboy95/aiautotech/pull/7) (`brokers-landing`, head `7e8b69ae`). GitHub Pages builds `main` only. There is no hosted preview. https://aiautotech.co.za/brokers/ returns **404** until #7 is published. That 404 is expected on this review. Do not merge to clear it.

Writing this page does not merge #7, does not publish the site, does not change a flag, and does not send. #7 stays open until Billy says yes to publish. Do not claim it is merged. `sending_enabled` stays false. Do not run ads. Do not start broker outreach from this page.

The CRM funnel is a different repo and a different yes: [CRM #85](https://github.com/billyboy95/ai-autotech-/pull/85) and its phone checklist [CRM #86](https://github.com/billyboy95/ai-autotech-/pull/86). Do not edit that repo from this visit. Do not merge those pull requests from here.

The front matter `published: false` tells GitHub Pages not to serve this file as a public page. The checklist still stands. This repo has no go-live runbook and no publish-decision page to link from.

## Which address is which

| Address | Role on this visit |
| --- | --- |
| `Willem@aiautotech.co.za` | The only From for AI AutoTech business email. Not used on this page. Do not send. |
| `billyfaber06@gmail.com` | On the site footer and the page schema. Never a From for a send from this visit. |
| `billy@aiautotech.co.za` | Old example. Do not use it. |

## Order

Do these in this order. A yes for one line is not a yes for the next.

1. Review #7 only. Look at the pull request. Do not open the live `/brokers/` URL as the page.
2. Stop until Billy says publish yes. This page does not merge #7.
3. After that publish, smoke https://aiautotech.co.za/brokers/ .
4. Confirm the audit, guide, and WhatsApp links on that page. Do not submit a form. Do not send the WhatsApp.
5. Never run ads or outreach without a separate yes. `sending_enabled` stays false.

If a later check is false, stop. Do not skip ahead.

## 1. Review #7 only

Look only. Do not tap **Merge**. Do not tap **Publish**.

1. Open https://github.com/billyboy95/aiautotech/pull/7
2. Pass for the gate: state is **Open**. Branch is `brokers-landing`. Head starts with `7e8b69ae`. If it is **Merged**, stop. Do not review a second publish.
3. Open **Files changed**. Read `brokers/index.html`. There is no Pages preview URL. A **404** on https://aiautotech.co.za/brokers/ is the live site today.
4. Pass for the look: the title names short-term insurance brokers in Gauteng. The H1 is **Quote requests answered in minutes, not tomorrow morning.** The legal line says AI AutoTech is not a financial services provider and does not give financial advice. The FAQ **Does it give financial advice?** starts with **No.**
5. Leave **Merge** untapped. A pass here is a review. It is not a publish.

## 2. Publish only when Billy says yes

[Website #7](https://github.com/billyboy95/aiautotech/pull/7) stays open. Do not merge it from the phone, from this page, or from this agent.

A yes to the look is not a publish yes. A publish yes is not a yes to ads and not a yes to outreach.

When he says yes, he merges #7 into `main` himself. Wait until that merge is the commit on `main` and GitHub Pages has rebuilt https://aiautotech.co.za . This page does not press Merge.

Also leave these unmerged: [aiautotech #4](https://github.com/billyboy95/aiautotech/pull/4) and [aiautotech #5](https://github.com/billyboy95/aiautotech/pull/5). The CRM note for those two is `docs/website-publish-decision.md` in `billyboy95/ai-autotech-`. Do not edit that file from here.

Reply he can send, one line:

- `publish #7 yes`

That line covers only website pull request #7.

## 3. Smoke https://aiautotech.co.za/brokers/

Skip this section while #7 is open.

After his publish yes, and after Pages has rebuilt `main`:

1. Open https://aiautotech.co.za/brokers/ in a private tab.
2. Pass: the page loads. The H1 is **Quote requests answered in minutes, not tomorrow morning.** The address bar is `https://aiautotech.co.za/brokers/`.
3. A **404** means Pages has not published that merge yet. Stop. Wait. Do not merge #7 again. Do not edit DNS. Do not change the CNAME. Pages stays on branch `main`.

Do not fill a form on this smoke. Do not tap a control that submits.

## 4. Confirm audit, guide, and WhatsApp

Run this only after section 3 showed the live page. Tap the link, confirm the destination, then come back. Do not send.

1. **Audit.** On the page, open **Take the 5-minute AI audit**. That href is `/audit/?utm_source=website&utm_medium=brokers_band&utm_campaign=free_ai_audit`. Pass: https://aiautotech.co.za/audit/ loads. The sticky **Book a free AI audit** link uses `utm_medium=brokers_sticky` and lands on the same audit page. Do not submit the audit form. Submitting emails Billy.
2. **Guide.** In the footer, open **Free AI guide** (`/guide/`). Pass: https://aiautotech.co.za/guide/ loads. Do not submit the guide form. Submitting emails Billy.
3. **WhatsApp.** The band button **WhatsApp Billy** is `https://wa.me/27646863803?text=Hi%20Billy%2C%20I%20run%20a%20short-term%20insurance%20brokerage%20and%20I%27d%20like%20the%20free%20AI%20audit.` Pass: WhatsApp opens a compose to +27 64 686 3803 with that text. Do not press send. Leave the chat. The green WhatsApp button uses the general site text. Do not send that one either.

A pass is the three destinations. It is not a lead. It is not a message sent.

## 5. Never ads or outreach without a separate yes

A publish yes for #7 is not a yes to advertise and not a yes to contact brokers.

- Do not create, unpause, or fund an ad on Google, Meta, TikTok, LinkedIn, or anywhere else. No spend. No card charge.
- Do not post or send under Billy's name. No email, SMS, or WhatsApp send.
- Broker outreach is [CRM #85](https://github.com/billyboy95/ai-autotech-/pull/85). Its phone steps are [CRM #86](https://github.com/billyboy95/ai-autotech-/pull/86) (`docs/phone-broker-outreach.md` in `billyboy95/ai-autotech-`). This page does not merge #85, does not import a CSV, and does not send. `sending_enabled` stays false. Drafts stay `draft_not_sent`.
- Do not change a flag. There is no website flag to turn on for `/brokers/`.

## Hard refuse

This visit refuses all of the following.

- Merging [website #7](https://github.com/billyboy95/aiautotech/pull/7) before Billy says `publish #7 yes`. This page does not merge it.
- Merging [aiautotech #4](https://github.com/billyboy95/aiautotech/pull/4) or [aiautotech #5](https://github.com/billyboy95/aiautotech/pull/5).
- Merging [CRM #85](https://github.com/billyboy95/ai-autotech-/pull/85) or editing `billyboy95/ai-autotech-`.
- Treating the live **404** on https://aiautotech.co.za/brokers/ as a reason to publish.
- A DNS edit, a CNAME edit, or a Pages source change. Pages stays on `main`.
- Submitting the audit form or the guide form on this visit.
- Sending the WhatsApp compose. Tapping **Send**, **Send now**, **Go live**, **Publish**, or **Post now**.
- Ad spend, a purchase, SMS credit, a phone number, or a card charge.
- Turning `sending_enabled` on. Setting any CRM flag. `AUTOMATION_SEND_ENABLED` stays unset, or stays the string `false`.
- A secret, key, token, password, or service-role value in git, a pull request, chat, or this file.

## Pass means

You opened pull request #7, or you stopped because it was not the open `brokers-landing` head `7e8b69ae`, and you did not tap **Merge**. On the review visit, https://aiautotech.co.za/brokers/ was still **404**, or you did not open it. You did not submit a form. You did not send a WhatsApp. You did not run an ad. `sending_enabled` stayed false. #7 is still open unless Billy already merged it himself.

If he later said `publish #7 yes` and you finished section 3, https://aiautotech.co.za/brokers/ loaded with the H1 **Quote requests answered in minutes, not tomorrow morning.** Section 4 then showed `/audit/`, `/guide/`, and a WhatsApp compose you did not send.

A pass does not mean #7 is merged, the page is live, a lead was captured, or anyone was contacted, unless those lines were on the screen after his yes.
