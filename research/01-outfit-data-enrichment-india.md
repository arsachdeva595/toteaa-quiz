# Research 01 — Enriching outfit data for Indian girls

_Status: draft v1 · Sep 2026 · scope: Phase 1 (quiz), groundwork for Phases 2–3_

## TL;DR

1. **Stop depending on Pinterest scraping.** Pinterest's ToS and Developer Terms both forbid automated scraping, and the official API is rate-limited and built for advertisers. Keep the old outfits.toteaa.com data only as internal reference. New outfit records should be **our own tagged records**. Images should come from sources we're allowed to use.
2. **What makes this product valuable is the tags, not the pictures.** A photo of a kurta is everywhere. A record that says _"works for a Haldi in humid Mumbai heat, parents present, under ₹2k, pairs with a mustard tote"_ is something nobody else has. Enrichment = adding **India-specific context tags** to every outfit.
3. **Build a controlled taxonomy first** (`data/taxonomy.json`), then tag every outfit against it using a vision-LLM pass plus a quick human check. The quiz, the upload mode (Phase 2) and mix-and-match (Phase 3) all read from the same tags.
4. **Privacy by design.** No accounts and no storage. Quiz answers live in memory or `sessionStorage` only. Phase 2 photos are processed in the browser where possible. Otherwise they go to a zero-retention API call and are never written to disk.

---

## 1. What Indian girls actually decide on (question research)

Western "what to wear" quizzes ask occasion, style and body type. For Indian girls (16–30, metro and tier-2), research on 2026 trend coverage, wedding guides and Gen Z style content shows extra factors that decide the outfit:

| Factor | Why it matters in India | Example answers |
|---|---|---|
| **Occasion (granular)** | "Wedding" alone isn't useful. Haldi, Mehendi, Sangeet, Pheras and Reception each have their own dress codes. | Haldi → yellow/mustard, washable. Mehendi → greens and florals. Sangeet → sequins and jewel tones. |
| **Who'll be there** | Dressing for parents or relatives is different from dressing for friends. This is the most "Indian" question and is missing from Western quizzes. | Family/relatives, friends only, colleagues, date, mixed |
| **Weather / region** | A Delhi December and a Chennai December are opposite problems. Monsoon means no long flared hems. | Hot and humid, dry heat, monsoon, cold, AC indoors |
| **Ethnic ↔ Western dial** | Indo-western is the default for Gen Z now: saree with a corset blouse and sneakers, lehenga skirt with a shirt, kurta with a jacket. | Full desi, Indo-western, full western |
| **Mood / vibe** | Drives colour and silhouette | Main character, soft & cute, boss, comfy/lazy, bold, minimal |
| **Comfort limits** | Dupatta handling, heels, how much skin | "No dupatta", "flats only", "covered shoulders" |
| **Budget / re-wear** | Repeat-wear and "already own it" matter a lot | Use what I have, under ₹1k, ₹1–3k, splurge |
| **Festival colour codes** | Navratri 9 colours (24 Sep–2 Oct 2026), Diwali, Holi whites, Onam kasavu, Pongal, Eid, Karva Chauth reds | Auto-suggest the colour of the day when the date matches |
| **Skin undertone (optional)** | Wheatish → mustard, terracotta, rust, olive, teal. Dusky → jewel tones (royal blue, magenta, emerald), plus rust and bright white. Universal: emerald, royal blue, teal, wine, ivory. | Warm / cool / neutral / skip. Ask as a choice, never infer it from a photo. |

**Quiz v1 design principle:** 6–8 taps, each one visual (chips/cards, no typing), and it should finish in under 60 seconds. The flow is in `data/quiz-v1.json`.

### Occasion list, India-first

- **Everyday:** college, office, WFH video call, running errands, travel/airport, gym-to-café
- **Social:** brunch, date night, birthday party, house party, concert/gig, clubbing, movie outing
- **Wedding functions:** roka/engagement, haldi, mehendi, sangeet, cocktail, wedding day (as a guest), reception
- **Festivals:** Diwali, Navratri/Garba, Durga Puja, Holi, Eid, Raksha Bandhan, Karva Chauth, Onam, Pongal, Ganesh Chaturthi, Lohri, Christmas/New Year
- **Family & religious:** temple/gurudwara visit, puja at home, family dinner, meeting the rishta family 👀
- **Milestones:** farewell (saree day!), college fest, interview, first day at work, graduation

### 2026 trend signals worth encoding as tags

- **Co-ord sets** are the defining Gen Z silhouette: western, chikankari, and sharara co-ords.
- **Indo-western fusion:** corset blouse with saree, lehenga skirt with a shirt or crop top, kurta with a denim jacket and chains, sneakers with ethnic wear.
- **Chikankari everywhere:** chikankari shirts with trousers for the office and brunch.
- **College uniform:** oversized graphic tee, wide-leg jeans and sneakers. Smart version: straight jeans, tucked shirt and loafers.
- **Wedding guests:** jewel tones or pastels. Avoid white, black and bridal red unless the host's dress code says otherwise.

---

## 2. Where outfit data can come from (ranked by safety × usefulness)

| # | Source | What we get | Licensing / risk | Use for |
|---|---|---|---|---|
| 1 | **Own curated records** (stylist-written or AI-assisted, human-checked) | Outfit = list of items + tags + styling note | Ours | ✅ Core library |
| 2 | **Own imagery:** flat-lays shot with Toteaa bags, AI-generated flat-lays or illustrations | Visuals for cards | Ours (check the AI tool's terms) | ✅ Quiz result cards, Phase 3 mix-and-match pieces |
| 3 | **Affiliate product feeds:** Myntra, Ajio, Nykaa Fashion, Amazon via affiliate networks such as Cuelinks, EarnKaro or Amazon Associates | Real, shoppable item images and prices | Allowed under affiliate terms, and it earns money | ✅ "Shop this look" links. Good for monetising |
| 4 | **UGC with consent:** Toteaa customers or community submitting looks through a form, with an explicit licence checkbox | Real Indian girls, real outfits | Needs a consent record, but no personal data beyond the image | ✅ Later, for social proof |
| 5 | **Polyvore Outfits dataset** (CC BY 4.0, ~68k outfits) | Item-to-item compatibility pairs, western only | Commercial use OK with attribution | ⚠️ Pairing rules and training a "does this go together" model. Not for display |
| 6 | **IndoFashion** (106k images, 15 Indian ethnic classes: saree, kurta, lehenga, palazzo, dupatta, blouse…) | Garment-type classifier training | Research dataset. Check the licence before any commercial use | ⚠️ Phase 2: detecting garments in uploads |
| 7 | **Myntra Kaggle scrapes** | Attribute vocabulary (neck types, prints, fabrics) | Scraped, murky provenance | ⚠️ Mine the **words** for our taxonomy only. Never ship their images |
| 8 | **Pinterest** | Trend discovery | ToS forbids scraping | ❌ Manual trend research only (a human browsing), never automated ingestion |
| 9 | **Google Trends (IN)** and Instagram hashtags, browsed manually | Which terms are rising (e.g. "chikankari co-ord", "corset blouse saree") | Fine for research | ✅ Monthly trend refresh of the `trend_tags` list |

**Recommendation:** start with **~150 hand-curated outfit records**. That covers occasions × vibes × ethnic dial, about 3 per important combination. Visuals should be AI flat-lays or illustrations in a consistent Toteaa style, and every outfit gets a tote pairing. Add affiliate "shop similar" links once the quiz shows traction.

---

## 3. Enrichment pipeline

```
 source item/outfit ──► normalise ──► vision-LLM tagger ──► human check (30s/outfit) ──► outfits.json
    (image + text)       (dedupe,       (fills schema fields     (fix wrong tags,          (static, versioned,
                          crop, bg)      from taxonomy only)      add styling note)         shipped with app)
```

1. **Normalise.** Dedupe with perceptual hashing, crop to a 4:5 ratio, and remove faces from the image or use flat-lays only. This avoids having identifiable people in our library at all.
2. **Tag with a vision LLM.** Give the model the image, `taxonomy.json` and a strict JSON schema (`data/schema/outfit.schema.json`). It may only choose values that exist in the taxonomy, which keeps tags consistent. Expected cost at 150–1,000 outfits is a few hundred rupees.
3. **Derived tags** are computed by code, not the model:
   - `climate_fit` from fabric: cotton, linen and chikankari are good for hot and humid weather. Velvet is not.
   - `modesty_level` from sleeve, neck and length.
   - `festival_colour_match` from palette × festival colour tables.
   - `tote_pairing` from palette and vibe × the Toteaa catalogue colours and themes.
4. **Human check.** A simple local review page shows the image, the tags as chips, and approve / fix buttons.
5. **Monthly trend refresh.** Update `trend_tags`, then re-rank outfits that match rising trends.

### Matching logic (Phase 1, no ML needed)

Score each outfit against the answers with weighted tag overlap:

```
score = 3·occasion + 2·ethnic_dial + 2·vibe + 1.5·weather + 1.5·company(modesty)
        + 1·budget + 1·comfort + bonus(festival_colour_today, trending)
```

Hard filters come first: comfort limits such as "no heels", and weather such as monsoon removing floor-length flares. Then return the top 3 with variety, meaning not three kurtas. Everything runs in the browser, so no server and no data leaves the device.

---

## 4. Privacy model (session-only)

| Phase | Data | Where it lives | Retention |
|---|---|---|---|
| 1 Quiz | Answers | JS memory or `sessionStorage` | Cleared when the tab closes |
| 2 Upload | Photo of self, reference, or wardrobe | In the browser (canvas). If a vision API is needed, it's sent over TLS to a provider with zero data retention. No logging of the image or payload on our side | Held only for the length of the request |
| 3 Mix & match | Chosen pieces, rendered collage | In the browser. "Save" = client-side PNG download. "Share" = Web Share API | Never uploaded unless the user shares it themselves |

- No login, no email and no analytics that include answers. If there's analytics at all, use cookieless aggregate counts such as Plausible or Umami: "quiz completed", "tote clicked".
- **Never infer** skin tone, body type or age from a photo. Always ask, and always allow "skip".
- Show a one-line promise on the start screen: _"Nothing you pick or upload is saved. Close the tab and it's gone."_

---

## 5. How the data carries into Phases 2 & 3

- **Phase 2 (upload):** the vision model describes the uploaded garment using the same taxonomy (garment, colour, fabric, vibe). We then match it to complementary outfit items and a tote. IndoFashion and Polyvore can later power an on-device classifier or compatibility model, so photos don't have to leave the device.
- **Phase 3 (mix & match):** each outfit record is split into **pieces** (top, bottom, layer, footwear, jewellery, bag). Every piece is its own tagged item with a transparent PNG. The same tags drive "what goes with this" suggestions. That's why the schema stores `items[]` from day one.

---

## 6. Next steps

1. Review `data/taxonomy.json` and `data/quiz-v1.json`. Add, cut or rename anything that doesn't sound like how your audience talks (Hinglish labels are welcome).
2. Share the Toteaa catalogue (colours, themes, SKUs) so `tote_pairing` can point to real bags.
3. Decide the image style: AI illustration, flat-lays shot in the Udaipur studio, or affiliate product images.
4. Curate the first 150 outfit records. `data/outfits.sample.json` shows the format.
5. Build the Phase 1 quiz UI as a static site with no backend.

---

### Sources

- Pinterest [Developer Terms](https://developers.pinterest.com/terms/) and [Terms of Service](https://policy.pinterest.com/en/terms-of-service): scraping is prohibited
- [IndoFashion paper (CVPRW 2021)](https://openaccess.thecvf.com/content/CVPR2021W/CVFAD/papers/Rajput_IndoFashion_Apparel_Classification_for_Indian_Ethnic_Clothes_CVPRW_2021_paper.pdf) · [GitHub](https://github.com/IndoFashion/IndoFashion) · [Kaggle](https://www.kaggle.com/datasets/validmodel/indo-fashion-dataset)
- [Polyvore Outfits on Hugging Face (CC BY 4.0)](https://huggingface.co/datasets/mvasil/polyvore-outfits) · [mmfashion compatibility docs](https://github.com/open-mmlab/mmfashion/blob/master/docs/dataset/FASHION_COMPATIBILITY_DATASET.md)
- [Myntra Fashion Product Dataset (Kaggle)](https://www.kaggle.com/datasets/djagatiya/myntra-fashion-product-dataset)
- Gen Z trends: [Pearl Academy](https://www.pearlacademy.com/blog/fashion/gen-z-female-fashion-trends), [idea-worldwide](https://idea-worldwide.com/blog/gen-z-fashion-trends-india/), [Cotton Culture ethnic trends 2026](https://www.cottonculture.co.in/blogs/news/ethnic-wear-trends-in-india-2026), [Ada Chikan co-ords](https://www.adachikan.com/blogs/news/chikankari-co-ord-sets-ethnic-fashion-trend-2026)
- Wedding dress codes: [Aza wedding guest guide 2026](https://www.azafashions.com/blog/what-to-wear-to-an-indian-wedding-the-complete-guest-style-guide-2026/), [Rashika Mittal function guide](https://rashikamittal.com/blogs/journal/indian-wedding-dress-code-every-function-guide), [W for Woman Haldi/Mehndi/Sangeet](https://www.wforwoman.com/blogs/blogs/what-to-wear-for-haldi-mehndi-sangeet-a-complete-summer-wedding-style-guide-for-women)
- Navratri 2026 colours: [Drik Panchang](https://www.drikpanchang.com/navratri/colors/navratri-nine-colors.html)
- Skin-tone colour guidance: [Bloomings](https://bloomings.in/clothing-colors-for-indian-skin-tone/), [Kaftanize](https://kaftanize.com/en-us/blogs/news/best-kurti-colors-every-indian-skin-tone)
