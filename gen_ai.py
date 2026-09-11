# -*- coding: utf-8 -*-
"""Generate ai-computing.html — 35kV Computing Power Cable marketing page, 11 languages, same style as solutions.html."""
import json, re

SRC = 'solutions.html'
OUT = 'ai-computing.html'

src = open(SRC, encoding='utf-8').read()

# ---- extract reusable pieces ----
style = src[src.find('<style>'):src.find('</style>') + 8]
topbar = src[src.find('<div class="topbar">'):src.find('</div>\n</div>', src.find('<div class="topbar">')) + 15]
contact_section = src[src.find('<section class="section" id="contact">'):src.find('</section>', src.find('<section class="section" id="contact">')) + 10]
footer = src[src.find('<footer>'):src.find('</footer>') + 9]
ldjs = src[src.find('<script type="application/ld+json">'):src.find('</script>', src.find('<script type="application/ld+json">')) + 9]
applyjs = src[src.find('<script>\nvar I18N'):src.find('</script>', src.find('<script>\nvar I18N')) + 9]

# ---- 11-language dictionary ----
T = {}

T['en'] = {
 'hero.eyebrow': 'Computing Power Cable · AI Data Centers · 2026',
 'hero.title': '35 kV Computing Power Cable — <span class="accent">Powering the AI Era</span>',
 'hero.sub': 'OUZHI Cable (欧智电缆) — Source Factory for 35 kV AI Data Center Cables',
 'hero.lead': 'AI GPU clusters, high-density racks and megawatt-scale data halls demand reliable medium-voltage power. OUZHI Cable engineers and manufactures 35 kV computing power cables — XLPE insulation, copper conductor, LSZH fire-safe sheath — from our own source factory in China, delivered to data centers worldwide.',
 'hero.cta1': 'Get Factory Quote', 'hero.cta2': 'View Technical Specs',
 'why.title': 'Why a Dedicated Computing Power Cable?',
 'why.p': 'AI data centers are no longer ordinary buildings — they are megawatt-scale power consumers. The medium-voltage cable feeding them must combine high ampacity, fire safety and long-term reliability.',
 'why.c1t': 'High-Density Power Delivery', 'why.c1d': 'Single-core 26/35 kV XLPE cables carry MW-scale loads from substation to AI cluster transformers, minimizing losses on long data-center feeder runs.',
 'why.c2t': 'Fire-Safe LSZH Construction', 'why.c2d': 'Low-smoke, zero-halogen sheath limits toxic smoke and corrosive gas in enclosed data halls — protecting people, servers and business continuity.',
 'why.c3t': 'Certified to Global Standards', 'why.c3d': 'Manufactured and 100% factory-tested to IEC 60502-2, GOST 31996 and GB/T 12706 — accepted by utilities and EPC contractors across target markets.',
 'why.c4t': 'Factory-Direct Speed & Price', 'why.c4d': 'Own production lines mean short lead times, custom drum lengths, and competitive factory pricing — no middlemen, no delays.',
 'spec.title': '35 kV Computing Power Cable — Technical Specifications',
 'spec.p': 'Standard configurations below; custom conductor sizes, lengths and screens available on request.',
 'spec.k1': 'Voltage rating', 'spec.v1': '26/35 kV (also 12/20 kV, 18/30 kV)',
 'spec.k2': 'Conductor', 'spec.v2': 'Copper (Cu) or aluminium (Al), class 2 stranded',
 'spec.k3': 'Insulation', 'spec.v3': 'XLPE (cross-linked polyethylene), triple-extrusion',
 'spec.k4': 'Screen', 'spec.v4': 'Copper wire / copper tape metallic screen',
 'spec.k5': 'Armour', 'spec.v5': 'SWA steel wire armouring (optional)',
 'spec.k6': 'Sheath', 'spec.v6': 'LSZH flame-retardant, low-smoke zero-halogen',
 'spec.k7': 'Standards', 'spec.v7': 'IEC 60502-2 · GOST 31996 · GB/T 12706',
 'spec.k8': 'Application', 'spec.v8': 'AI data centers, computing hubs, substation feeds, UPS rooms',
 'flow.title': 'From Our Factory to Your Data Center',
 'flow.p': 'A clear, trackable path from inquiry to energization — managed by our export engineering team.',
 'flow.s1t': 'Inquiry & Technical Proposal', 'flow.s1d': 'Send your voltage, load and layout — a tailored cable configuration and factory quote within 24 hours.',
 'flow.s2t': 'Contract & Production Plan', 'flow.s2d': 'Confirmed order enters our production schedule with an agreed delivery window.',
 'flow.s3t': 'Manufacturing & Full Testing', 'flow.s3d': 'Produced on our own lines; every drum 100% factory-tested before release.',
 'flow.s4t': 'Export Documentation', 'flow.s4d': 'Full export paperwork: certificates, packing lists, customs and EAC/CE documentation.',
 'flow.s5t': 'On-Time Delivery & Support', 'flow.s5d': 'Rail, road or sea to your site — with jointing, termination and installation guidance.',
 'serve.title': 'Serving AI Infrastructure Projects Worldwide',
 'serve.p': 'Export coverage across Central Asia · Middle East · Russia · Europe · Americas, including Uzbekistan, Kazakhstan, Turkey, Germany, Malaysia, Mexico and more.',
 'serve.th1': 'Region', 'serve.th2': 'Key Markets', 'serve.th3': 'What We Deliver',
 'serve.r1k': 'Central Asia', 'serve.r1m': 'Uzbekistan, Kazakhstan, Mongolia', 'serve.r1s': 'GOST-certified cables, EAC documents, rail & road delivery to site',
 'serve.r2k': 'Middle East', 'serve.r2m': 'UAE, Saudi Arabia, Turkey', 'serve.r2s': 'IEC-certified cables for data centers and smart-city projects',
 'serve.r3k': 'Russia & CIS', 'serve.r3m': 'Russia, Ukraine, Belarus', 'serve.r3s': 'Cold-resistant sheath options, EAC certification',
 'serve.r4k': 'Europe', 'serve.r4m': 'Germany, France, Spain, Portugal', 'serve.r4s': 'IEC 60502-2 cables with fast sea and rail logistics',
 'serve.r5k': 'Americas', 'serve.r5m': 'USA, Mexico, Brazil', 'serve.r5s': 'High-ampacity feeder cables, IEC-compliant manufacturing',
 'faq.title': 'FAQ — 35 kV Computing Power Cable',
 'faq.q1': 'What lead time can I expect?', 'faq.a1': 'Standard 35 kV cable orders ship within 3–5 weeks depending on volume and configuration; large projects can be scheduled to match your construction timeline.',
 'faq.q2': 'Do you provide export documentation and certifications?', 'faq.a2': 'Yes — IEC, GOST/EAC test certificates, packing lists, invoices and full customs documentation are included with every shipment.',
 'faq.q3': 'What is the minimum order quantity?', 'faq.a3': 'No fixed minimum for standard configurations — tell us your project needs and we will advise the most economical drum lengths.',
 'faq.q4': 'Can you supply custom conductor sizes and screens?', 'faq.a4': 'Yes. Our factory supports custom cross-sections, copper screens and armour options; send your specification for a free technical proposal.',
 'faq.q5': 'How do I get a fast price indication?', 'faq.a5': 'Email or WhatsApp your voltage, conductor, length and quantity — you will receive an indicative price within one business day.',
 'cta.title': 'Ready to Power Your AI Data Center?',
 'cta.p': 'Tell us your project location, voltage and cable requirements. Our export engineers will reply within 24 hours with a tailored solution and a factory-direct quotation.',
 'cta.email': 'Email: info@ouzcable.com', 'cta.phone': 'Phone: +998 99 851 6999',
 'cta.whatsapp': 'WhatsApp: +998 99 851 6999', 'cta.telegram': 'Telegram: @H99G99',
 'contact.email': 'Email:', 'contact.phone': 'Phone:', 'contact.whatsapp': 'WhatsApp:', 'contact.telegram': 'Telegram:',
 'contact.hq': 'HQ:', 'contact.hqval': 'China · Export Worldwide', 'contact.web': 'Website:',
 'footer.back': '← Back to OUZHI Cable Home', 'footer.rights': 'All rights reserved.',
}

T['zh'] = {
 'hero.eyebrow': '算力电缆 · AI 数据中心 · 2026',
 'hero.title': '35kV 算力电缆 — <span class="accent">为 AI 时代供电</span>',
 'hero.sub': '欧智电缆（OUZHI Cable）— 35kV AI 数据中心电缆源头工厂',
 'hero.lead': 'AI GPU 集群、高密度机柜与兆瓦级数据中心对中压供电提出严苛要求。欧智电缆依托自有源头工厂，设计并制造 35kV 算力电缆——XLPE 绝缘、铜导体、低烟无卤防火护套，从中国工厂直达全球数据中心。',
 'hero.cta1': '获取工厂报价', 'hero.cta2': '查看技术参数',
 'why.title': '为什么需要专用算力电缆？',
 'why.p': 'AI 数据中心已不是普通建筑，而是兆瓦级电力消费者。为其供电的中压电缆必须兼具大载流量、防火安全与长期可靠性。',
 'why.c1t': '高密度电力输送', 'why.c1d': '单芯 26/35kV XLPE 电缆将兆瓦级负荷从变电站输送至 AI 集群变压器，长距离馈线损耗更低。',
 'why.c2t': '低烟无卤防火结构', 'why.c2d': '低烟无卤护套在密闭数据机房内大幅减少有毒烟雾与腐蚀性气体，保护人员、服务器与业务连续性。',
 'why.c3t': '全球标准认证', 'why.c3d': '按 IEC 60502-2、GOST 31996、GB/T 12706 制造并 100% 出厂检测，获得目标市场电力公司与 EPC 承包商认可。',
 'why.c4t': '工厂直供，速度与价格', 'why.c4d': '自有生产线带来更短交期、定制盘长与竞争力的工厂价——无中间商、无延误。',
 'spec.title': '35kV 算力电缆 — 技术规格',
 'spec.p': '以下为标准配置；导体截面、长度与屏蔽层均可定制。',
 'spec.k1': '额定电压', 'spec.v1': '26/35kV（也可 12/20kV、18/30kV）',
 'spec.k2': '导体', 'spec.v2': '铜（Cu）或铝（Al），2 类绞合',
 'spec.k3': '绝缘', 'spec.v3': 'XLPE 交联聚乙烯（三层共挤）',
 'spec.k4': '屏蔽', 'spec.v4': '铜丝 / 铜带金属屏蔽',
 'spec.k5': '铠装', 'spec.v5': '钢丝铠装 SWA（可选）',
 'spec.k6': '护套', 'spec.v6': '低烟无卤阻燃 LSZH',
 'spec.k7': '执行标准', 'spec.v7': 'IEC 60502-2 · GOST 31996 · GB/T 12706',
 'spec.k8': '应用场景', 'spec.v8': 'AI 数据中心、算力中心、变电站馈线、UPS 机房',
 'flow.title': '从工厂到你的数据中心',
 'flow.p': '从询盘到送电，全程清晰可追溯——由我们的出口工程团队管理。',
 'flow.s1t': '询盘与技术方案', 'flow.s1d': '告知电压、负荷与布局，24 小时内获得定制电缆配置与工厂报价。',
 'flow.s2t': '签约与生产计划', 'flow.s2d': '确认订单进入生产排程，并约定交付窗口。',
 'flow.s3t': '生产与全检', 'flow.s3d': '自有生产线制造，每盘电缆出厂前 100% 检测。',
 'flow.s4t': '出口单证', 'flow.s4d': '完整出口文件：证书、装箱单、报关及 EAC/CE 文档。',
 'flow.s5t': '准时交付与支持', 'flow.s5d': '铁路、公路或海运直达现场，并提供接头、终端与敷设指导。',
 'serve.title': '服务全球 AI 基础设施项目',
 'serve.p': '出口覆盖中亚 · 中东 · 俄罗斯 · 欧洲 · 美洲，包括乌兹别克斯坦、哈萨克斯坦、土耳其、德国、马来西亚、墨西哥等。',
 'serve.th1': '区域', 'serve.th2': '重点市场', 'serve.th3': '交付内容',
 'serve.r1k': '中亚', 'serve.r1m': '乌兹别克斯坦、哈萨克斯坦、蒙古', 'serve.r1s': 'GOST 认证电缆、EAC 文件、铁路与公路直送现场',
 'serve.r2k': '中东', 'serve.r2m': '阿联酋、沙特、土耳其', 'serve.r2s': 'IEC 认证电缆，用于数据中心与智慧城市项目',
 'serve.r3k': '俄罗斯与独联体', 'serve.r3m': '俄罗斯、乌克兰、白俄罗斯', 'serve.r3s': '耐寒护套选项、EAC 认证',
 'serve.r4k': '欧洲', 'serve.r4m': '德国、法国、西班牙、葡萄牙', 'serve.r4s': 'IEC 60502-2 电缆，海运与铁路物流快捷',
 'serve.r5k': '美洲', 'serve.r5m': '美国、墨西哥、巴西', 'serve.r5s': '大载流量馈线电缆、符合 IEC 的制造',
 'faq.title': '常见问题 — 35kV 算力电缆',
 'faq.q1': '交期大概多久？', 'faq.a1': '标准 35kV 电缆订单视数量与配置 3–5 周出货；大型项目可按您的施工进度排产。',
 'faq.q2': '是否提供出口单证与认证？', 'faq.a2': '提供。每批货物均附带 IEC、GOST/EAC 测试证书、装箱单、发票及完整报关文件。',
 'faq.q3': '起订量是多少？', 'faq.a3': '标准配置无固定起订量——告知项目需求，我们将建议最经济的盘长。',
 'faq.q4': '能否定制导体截面与屏蔽？', 'faq.a4': '可以。工厂支持定制截面、铜屏蔽与铠装选项，发送规格即可获得免费技术方案。',
 'faq.q5': '如何快速获得价格？', 'faq.a5': '通过邮件或 WhatsApp 告知电压、导体、长度与数量，一个工作日内回复参考价。',
 'cta.title': '准备为你的 AI 数据中心供电？',
 'cta.p': '告诉我们项目地点、电压与电缆需求。出口工程师将在 24 小时内回复定制方案与工厂直供报价。',
 'cta.email': '邮箱: info@ouzcable.com', 'cta.phone': '电话: +998 99 851 6999',
 'cta.whatsapp': 'WhatsApp: +998 99 851 6999', 'cta.telegram': 'Telegram: @H99G99',
 'contact.email': '邮箱:', 'contact.phone': '电话:', 'contact.whatsapp': 'WhatsApp:', 'contact.telegram': 'Telegram:',
 'contact.hq': '总部:', 'contact.hqval': '中国 · 全球出口', 'contact.web': '网站:',
 'footer.back': '← 返回欧智电缆首页', 'footer.rights': '版权所有。',
}

T['ru'] = {
 'hero.eyebrow': 'Кабели для вычислений · Центры обработки данных · 2026',
 'hero.title': 'Кабель 35 кВ для вычислительных центров — <span class="accent">Энергия для эры ИИ</span>',
 'hero.sub': 'OUZHI Cable (欧智电缆) — завод-изготовитель кабелей 35 кВ для ЦОД и ИИ',
 'hero.lead': 'GPU-кластеры, стойки высокой плотности и дата-центры мегаваттного класса требуют надёжного среднего напряжения. OUZHI Cable проектирует и производит кабели 35 кВ для вычислительных мощностей — изоляция XLPE, медная жила, огнестойкая оболочка LSZH — на собственном заводе в Китае, с доставкой в дата-центры по всему миру.',
 'hero.cta1': 'Получить цену завода', 'hero.cta2': 'Технические параметры',
 'why.title': 'Почему нужен специальный кабель для вычислений?',
 'why.p': 'Дата-центры ИИ — уже не обычные здания, а потребители мегаваттного масштаба. Питающий их кабель среднего напряжения должен сочетать высокую токовую нагрузку, пожарную безопасность и долговечность.',
 'why.c1t': 'Передача мощности высокой плотности', 'why.c1d': 'Одножильные кабели 26/35 кВ XLPE передают мегаваттные нагрузки от подстанции к трансформаторам ИИ-кластеров с минимальными потерями.',
 'why.c2t': 'Пожаробезопасная конструкция LSZH', 'why.c2d': 'Оболочка LSZH ограничивает токсичный дым и коррозионные газы в закрытых машинных залах — защищает людей, серверы и непрерывность бизнеса.',
 'why.c3t': 'Сертификация по мировым стандартам', 'why.c3d': 'Производство и 100% заводской контроль по IEC 60502-2, GOST 31996 и GB/T 12706 — признано энергокомпаниями и EPC-подрядчиками.',
 'why.c4t': 'Скорость и цена завода-изготовителя', 'why.c4d': 'Собственные линии — короткие сроки, индивидуальные длины барабанов и конкурентоспособные цены — без посредников.',
 'spec.title': 'Кабель 35 кВ для вычислений — технические характеристики',
 'spec.p': 'Ниже стандартные конфигурации; сечение, длины и экраны — по запросу.',
 'spec.k1': 'Номинальное напряжение', 'spec.v1': '26/35 кВ (также 12/20 кВ, 18/30 кВ)',
 'spec.k2': 'Жила', 'spec.v2': 'Медь (Cu) или алюминий (Al), класс 2',
 'spec.k3': 'Изоляция', 'spec.v3': 'XLPE (сшитый полиэтилен), тройная экструзия',
 'spec.k4': 'Экран', 'spec.v4': 'Медный проволочный / ленточный экран',
 'spec.k5': 'Броня', 'spec.v5': 'Стальная проволочная броня SWA (опционально)',
 'spec.k6': 'Оболочка', 'spec.v6': 'LSZH огнестойкая, безгалогенная',
 'spec.k7': 'Стандарты', 'spec.v7': 'IEC 60502-2 · GOST 31996 · GB/T 12706',
 'spec.k8': 'Применение', 'spec.v8': 'Дата-центры ИИ, вычислительные центры, питание подстанций, ИБП-помещения',
 'flow.title': 'От нашего завода до вашего дата-центра',
 'flow.p': 'Прозрачный путь от запроса до ввода в эксплуатацию — под управлением нашей экспортной инженерной команды.',
 'flow.s1t': 'Запрос и техническое предложение', 'flow.s1d': 'Укажите напряжение, нагрузку и схему — конфигурация кабеля и цена завода в течение 24 часов.',
 'flow.s2t': 'Контракт и план производства', 'flow.s2d': 'Подтверждённый заказ входит в производственный график с согласованным сроком.',
 'flow.s3t': 'Производство и полный контроль', 'flow.s3d': 'Выпуск на собственных линиях; каждый барабан 100% протестирован перед отгрузкой.',
 'flow.s4t': 'Экспортная документация', 'flow.s4d': 'Полный пакет: сертификаты, упаковочные листы, таможенные и EAC/CE документы.',
 'flow.s5t': 'Своевременная поставка и поддержка', 'flow.s5d': 'Железная дорога, авто или море до объекта — с рекомендациями по монтажу и оконцеванию.',
 'serve.title': 'Обслуживание проектов ИИ-инфраструктуры по всему миру',
 'serve.p': 'Экспорт в Центральную Азию · Ближний Восток · Россию · Европу · Америку, включая Узбекистан, Казахстан, Турцию, Германию, Малайзию, Мексику и др.',
 'serve.th1': 'Регион', 'serve.th2': 'Ключевые рынки', 'serve.th3': 'Что мы поставляем',
 'serve.r1k': 'Центральная Азия', 'serve.r1m': 'Узбекистан, Казахстан, Монголия', 'serve.r1s': 'Кабели с сертификатами ГОСТ, документы EAC, доставка ЖД и авто',
 'serve.r2k': 'Ближний Восток', 'serve.r2m': 'ОАЭ, Саудовская Аравия, Турция', 'serve.r2s': 'Кабели IEC для дата-центров и умных городов',
 'serve.r3k': 'Россия и СНГ', 'serve.r3m': 'Россия, Украина, Беларусь', 'serve.r3s': 'Холодостойкие оболочки, сертификация EAC',
 'serve.r4k': 'Европа', 'serve.r4m': 'Германия, Франция, Испания, Португалия', 'serve.r4s': 'Кабели IEC 60502-2, быстрая морская и ЖД логистика',
 'serve.r5k': 'Америка', 'serve.r5m': 'США, Мексика, Бразилия', 'serve.r5s': 'Кабели с высокой нагрузкой, производство по IEC',
 'faq.title': 'FAQ — кабель 35 кВ для вычислений',
 'faq.q1': 'Каков срок поставки?', 'faq.a1': 'Стандартные заказы 35 кВ отгружаются за 3–5 недель в зависимости от объёма; крупные проекты согласуем с графиком строительства.',
 'faq.q2': 'Предоставляете ли экспортные документы и сертификаты?', 'faq.a2': 'Да — сертификаты IEC, GOST/EAC, упаковочные листы, инвойсы и таможенная документация прилагаются к каждой поставке.',
 'faq.q3': 'Каков минимальный объём заказа?', 'faq.a3': 'Для стандартных конфигураций фиксированного минимума нет — укажите потребности проекта, предложим экономичные длины.',
 'faq.q4': 'Возможны ли нестандартные сечения и экраны?', 'faq.a4': 'Да. Завод поддерживает индивидуальные сечения, медные экраны и броню; пришлите спецификацию — получите бесплатное предложение.',
 'faq.q5': 'Как быстро получить цену?', 'faq.a5': 'Пришлите по email или WhatsApp напряжение, сечение, длину и количество — ориентировочная цена в течение одного рабочего дня.',
 'cta.title': 'Готовы обеспечить энергией ваш дата-центр ИИ?',
 'cta.p': 'Сообщите локацию проекта, напряжение и требования к кабелю. Экспортные инженеры ответят в течение 24 часов с решением и ценой завода.',
 'cta.email': 'Email: info@ouzcable.com', 'cta.phone': 'Тел: +998 99 851 6999',
 'cta.whatsapp': 'WhatsApp: +998 99 851 6999', 'cta.telegram': 'Telegram: @H99G99',
 'contact.email': 'Email:', 'contact.phone': 'Тел:', 'contact.whatsapp': 'WhatsApp:', 'contact.telegram': 'Telegram:',
 'contact.hq': 'Головной офис:', 'contact.hqval': 'Китай · Экспорт по всему миру', 'contact.web': 'Сайт:',
 'footer.back': '← На главную OUZHI Cable', 'footer.rights': 'Все права защищены.',
}

T['ar'] = {
 'hero.eyebrow': 'كابل قوة الحوسبة · مراكز البيانات · 2026',
 'hero.title': 'كابل قوة الحوسبة 35 ك.ف — <span class="accent">طاقة لعصر الذكاء الاصطناعي</span>',
 'hero.sub': 'OUZHI Cable (欧智电缆) — المصنع المصدر لكابلات 35 ك.ف لمراكز بيانات الذكاء الاصطناعي',
 'hero.lead': 'مجموعات GPU والرفوف عالية الكثافة وقاعات البيانات بمقياس ميغاواط تتطلب طاقة موثوقة بالجهد المتوسط. تصمم وتصنع OUZHI Cable كابلات قوة الحوسبة 35 ك.ف — عزل XLPE، ناقل نحاسي، غلاف LSZH مقاوم للحريق — من مصنعنا المصدر في الصين، مع توصيل لمراكز البيانات حول العالم.',
 'hero.cta1': 'احصل على سعر المصنع', 'hero.cta2': 'عرض المواصفات الفنية',
 'why.title': 'لماذا كابل مخصص لقوة الحوسبة؟',
 'why.p': 'مراكز بيانات الذكاء الاصطناعي لم تعد مبانٍ عادية — بل مستهلكة للطاقة بمقياس ميغاواط. يجب أن يجمع كابل الجهد المتوسط المغذي لها بين السعة العالية والأمان من الحرائق والموثوقية طويلة الأمد.',
 'why.c1t': 'نقل طاقة عالي الكثافة', 'why.c1d': 'كابلات XLPE أحادية النواة 26/35 ك.ف تنقل أحمال ميغاواط من المحطة إلى محولات مجموعات الذكاء الاصطناعي بأقل خسائر.',
 'why.c2t': 'بنية LSZH مقاومة للحريق', 'why.c2d': 'غلاف LSZH يحد من الدخان السام والغازات المسببة للتآكل في قاعات البيانات المغلقة — حماية للأفراد والخوادم واستمرارية الأعمال.',
 'why.c3t': 'معتمدة وفق المعايير العالمية', 'why.c3d': 'تصنيع واختبار 100% في المصنع وفق IEC 60502-2 وGOST 31996 وGB/T 12706 — مقبولة من شركات الكهرباء ومقاولي EPC.',
 'why.c4t': 'سرعة وسعر المصنع المباشر', 'why.c4d': 'خطوط إنتاج خاصة تعني مهل قصيرة وأطوال براميل مخصصة وأسعار تنافسية — بدون وسطاء.',
 'spec.title': 'كابل قوة الحوسبة 35 ك.ف — المواصفات الفنية',
 'spec.p': 'التكوينات القياسية أدناه؛ المقاطع والأطوال والدرع قابلة للتخصيص.',
 'spec.k1': 'الجهد الاسمي', 'spec.v1': '26/35 ك.ف (وأيضاً 12/20، 18/30 ك.ف)',
 'spec.k2': 'الناقل', 'spec.v2': 'نحاس (Cu) أو ألمنيوم (Al)، فئة 2',
 'spec.k3': 'العزل', 'spec.v3': 'XLPE (بولي إيثيلين مترابط)، بثق ثلاثي',
 'spec.k4': 'الدرع', 'spec.v4': 'درع معدني من أسلاك/شريط نحاسي',
 'spec.k5': 'التسليح', 'spec.v5': 'تسليح أسلاك فولاذية SWA (اختياري)',
 'spec.k6': 'الغلاف', 'spec.v6': 'LSZH مقاوم للحريق خالٍ من الهالوجين',
 'spec.k7': 'المعايير', 'spec.v7': 'IEC 60502-2 · GOST 31996 · GB/T 12706',
 'spec.k8': 'الاستخدام', 'spec.v8': 'مراكز بيانات الذكاء الاصطناعي، مراكز الحوسبة، تغذية المحطات، غرف UPS',
 'flow.title': 'من مصنعنا إلى مركز بياناتك',
 'flow.p': 'مسار واضح وقابل للتتبع من الاستفسار حتى التشغيل — يديره فريقنا الهندسي للتصدير.',
 'flow.s1t': 'الاستفسار والعرض الفني', 'flow.s1d': 'أرسل الجهد والحمل والتخطيط — تكوين كابل مخصص وسعر المصنع خلال 24 ساعة.',
 'flow.s2t': 'العقد وخطة الإنتاج', 'flow.s2d': 'يدخل الطلب المؤكد جدول الإنتاج بنافذة تسليم متفق عليها.',
 'flow.s3t': 'التصنيع والفحص الكامل', 'flow.s3d': 'إنتاج على خطوطنا الخاصة؛ كل بكرة مختبَرة 100% قبل الإفراج.',
 'flow.s4t': 'وثائق التصدير', 'flow.s4d': 'حزمة تصدير كاملة: شهادات وقوائم تعبئة وجمارك ووثائق EAC/CE.',
 'flow.s5t': 'التسليم في الوقت المحدد والدعم', 'flow.s5d': 'سكة حديد أو بر أو بحر إلى موقعك — مع إرشادات الوصل والإنهاء والتركيب.',
 'serve.title': 'خدمة مشاريع البنية التحتية للذكاء الاصطناعي عالمياً',
 'serve.p': 'تغطية تصدير عبر آسيا الوسطى · الشرق الأوسط · روسيا · أوروبا · الأمريكتين، بما في ذلك أوزبكستان وكازاخستان وتركيا وألمانيا وماليزيا والمكسيك وغيرها.',
 'serve.th1': 'المنطقة', 'serve.th2': 'الأسواق الرئيسية', 'serve.th3': 'ما نقدمه',
 'serve.r1k': 'آسيا الوسطى', 'serve.r1m': 'أوزبكستان، كازاخستان، منغوليا', 'serve.r1s': 'كابلات معتمدة GOST ووثائق EAC وتسليم بالسكك الحديدية والطرق',
 'serve.r2k': 'الشرق الأوسط', 'serve.r2m': 'الإمارات، السعودية، تركيا', 'serve.r2s': 'كابلات معتمدة IEC لمراكز البيانات والمشاريع الذكية',
 'serve.r3k': 'روسيا ورابطة الدول', 'serve.r3m': 'روسيا، أوكرانيا، بيلاروسيا', 'serve.r3s': 'خيارات أغلفة مقاومة للبرد، شهادة EAC',
 'serve.r4k': 'أوروبا', 'serve.r4m': 'ألمانيا، فرنسا، إسبانيا، البرتغال', 'serve.r4s': 'كابلات IEC 60502-2 مع لوجستيات بحرية وسكك سريعة',
 'serve.r5k': 'الأمريكتان', 'serve.r5m': 'الولايات المتحدة، المكسيك، البرازيل', 'serve.r5s': 'كابلات تغذية عالية السعة، تصنيع متوافق مع IEC',
 'faq.title': 'الأسئلة الشائعة — كابل قوة الحوسبة 35 ك.ف',
 'faq.q1': 'كم تبلغ مدة التسليم؟', 'faq.a1': 'شحن الطلبات القياسية 35 ك.ف خلال 3–5 أسابيع حسب الحجم؛ ويمكن جدولة المشاريع الكبيرة بما يناسب جدول إنشائكم.',
 'faq.q2': 'هل توفرون وثائق التصدير والشهادات؟', 'faq.a2': 'نعم — شهادات IEC وGOST/EAC وقوائم التعبئة والفواتير ووثائق الجمارك الكاملة مع كل شحنة.',
 'faq.q3': 'ما هو الحد الأدنى للطلب؟', 'faq.a3': 'لا حد أدنى ثابت للتكوينات القياسية — أخبرنا باحتياجات مشروعك وسنقترح أطوال البراميل الأكثر اقتصاداً.',
 'faq.q4': 'هل يمكن توفير مقاطع وأدرع مخصصة؟', 'faq.a4': 'نعم. يدعم مصنعنا المقاطع المخصصة والأدرع النحاسية وخيارات التسليح؛ أرسل المواصفات لعرض فني مجاني.',
 'faq.q5': 'كيف أحصل على سعر سريع؟', 'faq.a5': 'أرسل بالبريد أو واتساب الجهد والمقطع والطول والكمية — سعر استرشادي خلال يوم عمل واحد.',
 'cta.title': 'مستعد لتزويد مركز بيانات الذكاء الاصطناعي بالطاقة؟',
 'cta.p': 'أخبرنا بموقع مشروعك والجهد ومتطلبات الكابل. سيرد مهندسو التصدير خلال 24 ساعة بحل مخصص وسعر مباشر من المصنع.',
 'cta.email': 'البريد: info@ouzcable.com', 'cta.phone': 'الهاتف: +998 99 851 6999',
 'cta.whatsapp': 'واتساب: +998 99 851 6999', 'cta.telegram': 'تيليجرام: @H99G99',
 'contact.email': 'البريد:', 'contact.phone': 'الهاتف:', 'contact.whatsapp': 'واتساب:', 'contact.telegram': 'تيليجرام:',
 'contact.hq': 'المقر:', 'contact.hqval': 'الصين · تصدير عالمي', 'contact.web': 'الموقع:',
 'footer.back': '← العودة إلى الرئيسية OUZHI Cable', 'footer.rights': 'جميع الحقوق محفوظة.',
}

T['fr'] = {
 'hero.eyebrow': 'Câble de puissance de calcul · Data centers IA · 2026',
 'hero.title': 'Câble 35 kV pour puissance de calcul — <span class="accent">Alimenter l\u2019ère de l\u2019IA</span>',
 'hero.sub': 'OUZHI Cable (欧智电缆) — usine source de câbles 35 kV pour data centers IA',
 'hero.lead': 'Les clusters GPU, les racks haute densité et les salles de données à l\u2019échelle du mégawatt exigent une alimentation moyenne tension fiable. OUZHI Cable conçoit et fabrique des câbles de puissance de calcul 35 kV — isolation XLPE, conducteur cuivre, gaine LSZH ignifuge — dans notre usine source en Chine, livrés dans le monde entier.',
 'hero.cta1': 'Obtenir un prix usine', 'hero.cta2': 'Voir les spécifications',
 'why.title': 'Pourquoi un câble dédié à la puissance de calcul ?',
 'why.p': 'Les data centers IA ne sont plus des bâtiments ordinaires — ce sont des consommateurs au mégawatt. Le câble moyenne tension qui les alimente doit allier forte ampacité, sécurité incendie et fiabilité à long terme.',
 'why.c1t': 'Distribution haute densité', 'why.c1d': 'Les câbles unipolaires 26/35 kV XLPE transportent des charges MW de la sous-station aux transformateurs des clusters IA avec un minimum de pertes.',
 'why.c2t': 'Construction LSZH ignifuge', 'why.c2d': 'La gaine LSZH limite fumées toxiques et gaz corrosifs dans les salles fermées — protégeant personnes, serveurs et continuité d\u2019activité.',
 'why.c3t': 'Certifiée aux normes mondiales', 'why.c3d': 'Fabriqué et testé à 100% en usine selon IEC 60502-2, GOST 31996 et GB/T 12706 — accepté par les utilités et les EPC.',
 'why.c4t': 'Vitesse et prix d\u2019usine', 'why.c4d': 'Lignes de production propres : délais courts, longueurs de touret personnalisées et prix d\u2019usine compétitifs — sans intermédiaires.',
 'spec.title': 'Câble 35 kV puissance de calcul — spécifications techniques',
 'spec.p': 'Configurations standard ci-dessous ; sections, longueurs et écrans sur demande.',
 'spec.k1': 'Tension nominale', 'spec.v1': '26/35 kV (aussi 12/20 kV, 18/30 kV)',
 'spec.k2': 'Conducteur', 'spec.v2': 'Cuivre (Cu) ou aluminium (Al), classe 2',
 'spec.k3': 'Isolation', 'spec.v3': 'XLPE (polyéthylène réticulé), triple extrusion',
 'spec.k4': 'Écran', 'spec.v4': 'Écran métallique fils / feuillard cuivre',
 'spec.k5': 'Armure', 'spec.v5': 'Armure fils d\u2019acier SWA (option)',
 'spec.k6': 'Gaine', 'spec.v6': 'LSZH ignifuge, sans halogène',
 'spec.k7': 'Normes', 'spec.v7': 'IEC 60502-2 · GOST 31996 · GB/T 12706',
 'spec.k8': 'Application', 'spec.v8': 'Data centers IA, hubs de calcul, alimentation sous-stations, salles UPS',
 'flow.title': 'De notre usine à votre data center',
 'flow.p': 'Un parcours clair et traçable, de la demande à la mise sous tension — géré par notre équipe d\u2019ingénierie export.',
 'flow.s1t': 'Demande et proposition technique', 'flow.s1d': 'Envoyez tension, charge et plan — configuration sur mesure et prix usine sous 24 h.',
 'flow.s2t': 'Contrat et plan de production', 'flow.s2d': 'La commande confirmée entre au planning avec un délai convenu.',
 'flow.s3t': 'Fabrication et tests complets', 'flow.s3d': 'Produit sur nos lignes ; chaque touret 100% testé en usine.',
 'flow.s4t': 'Documentation export', 'flow.s4d': 'Dossier complet : certificats, listes de colisage, douane, documents EAC/CE.',
 'flow.s5t': 'Livraison à temps et support', 'flow.s5d': 'Rail, route ou mer jusqu\u2019au site — avec conseils de jonction, terminaison et pose.',
 'serve.title': 'Au service des projets d\u2019infrastructure IA dans le monde',
 'serve.p': 'Couverture export : Asie centrale · Moyen-Orient · Russie · Europe · Amériques, dont Ouzbékistan, Kazakhstan, Turquie, Allemagne, Malaisie, Mexique et plus.',
 'serve.th1': 'Région', 'serve.th2': 'Marchés clés', 'serve.th3': 'Ce que nous livrons',
 'serve.r1k': 'Asie centrale', 'serve.r1m': 'Ouzbékistan, Kazakhstan, Mongolie', 'serve.r1s': 'Câbles certifiés GOST, documents EAC, livraison rail et route',
 'serve.r2k': 'Moyen-Orient', 'serve.r2m': 'EAU, Arabie saoudite, Turquie', 'serve.r2s': 'Câbles certifiés IEC pour data centers et villes intelligentes',
 'serve.r3k': 'Russie et CEI', 'serve.r3m': 'Russie, Ukraine, Biélorussie', 'serve.r3s': 'Gaines résistantes au froid, certification EAC',
 'serve.r4k': 'Europe', 'serve.r4m': 'Allemagne, France, Espagne, Portugal', 'serve.r4s': 'Câbles IEC 60502-2, logistique maritime et ferroviaire rapide',
 'serve.r5k': 'Amériques', 'serve.r5m': 'États-Unis, Mexique, Brésil', 'serve.r5s': 'Câbles forte ampacité, fabrication conforme IEC',
 'faq.title': 'FAQ — câble 35 kV puissance de calcul',
 'faq.q1': 'Quel délai de livraison ?', 'faq.a1': 'Commandes standard 35 kV : expédition sous 3–5 semaines selon volume ; grands projets planifiés selon votre calendrier.',
 'faq.q2': 'Fournissez-vous documents export et certifications ?', 'faq.a2': 'Oui — certificats IEC, GOST/EAC, listes de colisage, factures et douane inclus à chaque expédition.',
 'faq.q3': 'Quantité minimale de commande ?', 'faq.a3': 'Pas de minimum fixe pour les configurations standard — indiquez vos besoins, nous conseillons les longueurs les plus économiques.',
 'faq.q4': 'Sections et écrans personnalisés ?', 'faq.a4': 'Oui. L\u2019usine supporte sections sur mesure, écrans cuivre et armures ; envoyez votre spécification pour une proposition gratuite.',
 'faq.q5': 'Comment obtenir un prix rapide ?', 'faq.a5': 'Email ou WhatsApp avec tension, section, longueur et quantité — prix indicatif sous un jour ouvré.',
 'cta.title': 'Prêt à alimenter votre data center IA ?',
 'cta.p': 'Indiquez localisation, tension et besoins. Nos ingénieurs export répondent sous 24 h avec solution sur mesure et prix d\u2019usine.',
 'cta.email': 'Email : info@ouzcable.com', 'cta.phone': 'Tél : +998 99 851 6999',
 'cta.whatsapp': 'WhatsApp : +998 99 851 6999', 'cta.telegram': 'Telegram : @H99G99',
 'contact.email': 'Email :', 'contact.phone': 'Tél :', 'contact.whatsapp': 'WhatsApp :', 'contact.telegram': 'Telegram :',
 'contact.hq': 'Siège :', 'contact.hqval': 'Chine · Export mondial', 'contact.web': 'Site :',
 'footer.back': '← Retour à l\u2019accueil OUZHI Cable', 'footer.rights': 'Tous droits réservés.',
}

T['de'] = {
 'hero.eyebrow': 'Rechenleistungskabel · KI-Rechenzentren · 2026',
 'hero.title': '35-kV-Rechenleistungskabel — <span class="accent">Energie für das KI-Zeitalter</span>',
 'hero.sub': 'OUZHI Cable (欧智电缆) — Quellenwerk für 35-kV-Kabel für KI-Rechenzentren',
 'hero.lead': 'KI-GPU-Cluster, Hochdichte-Racks und Megawatt-Datenhallen benötigen zuverlässige Mittelspannungsversorgung. OUZHI Cable konstruiert und fertigt 35-kV-Rechenleistungskabel — XLPE-Isolierung, Kupferleiter, LSZH-Brandschutzmantel — im eigenen Quellenwerk in China, weltweit geliefert.',
 'hero.cta1': 'Werkspreis anfragen', 'hero.cta2': 'Technische Daten',
 'why.title': 'Warum ein dediziertes Rechenleistungskabel?',
 'why.p': 'KI-Rechenzentren sind keine gewöhnlichen Gebäude mehr — sie sind Stromverbraucher im Megawatt-Maßstab. Das sie versorgende Mittelspannungskabel muss hohe Strombelastbarkeit, Brandschutz und Langzeitzuverlässigkeit vereinen.',
 'why.c1t': 'Hochdichte Energieübertragung', 'why.c1d': 'Einadrige 26/35-kV-XLPE-Kabel transportieren MW-Lasten vom Umspannwerk zu KI-Cluster-Transformatoren mit minimalen Verlusten.',
 'why.c2t': 'Brandsichere LSZH-Konstruktion', 'why.c2d': 'LSZH-Mantel begrenzt giftigen Rauch und korrosive Gase in geschlossenen Datenhallen — Schutz für Menschen, Server und Geschäftskontinuität.',
 'why.c3t': 'Nach globalen Normen zertifiziert', 'why.c3d': 'Gefertigt und 100% werksgeprüft nach IEC 60502-2, GOST 31996 und GB/T 12706 — akzeptiert von Versorgern und EPC-Auftragnehmern.',
 'why.c4t': 'Werksdirekte Schnelligkeit und Preise', 'why.c4d': 'Eigene Produktionslinien bedeuten kurze Lieferzeiten, kundenspezifische Trommellängen und wettbewerbsfähige Werkspreise — ohne Zwischenhändler.',
 'spec.title': '35-kV-Rechenleistungskabel — technische Daten',
 'spec.p': 'Standardkonfigurationen unten; Querschnitte, Längen und Schirme auf Anfrage.',
 'spec.k1': 'Nennspannung', 'spec.v1': '26/35 kV (auch 12/20 kV, 18/30 kV)',
 'spec.k2': 'Leiter', 'spec.v2': 'Kupfer (Cu) oder Aluminium (Al), Klasse 2',
 'spec.k3': 'Isolierung', 'spec.v3': 'XLPE (vernetztes Polyethylen), Dreifach-Extrusion',
 'spec.k4': 'Schirm', 'spec.v4': 'Kupferdraht-/Band-Metallschirm',
 'spec.k5': 'Bewehrung', 'spec.v5': 'Stahldrahtbewehrung SWA (optional)',
 'spec.k6': 'Mantel', 'spec.v6': 'LSZH flammwidrig, halogenfrei',
 'spec.k7': 'Normen', 'spec.v7': 'IEC 60502-2 · GOST 31996 · GB/T 12706',
 'spec.k8': 'Anwendung', 'spec.v8': 'KI-Rechenzentren, Rechenzentren, Umspannwerkspeisungen, USV-Räume',
 'flow.title': 'Von unserem Werk in Ihr Rechenzentrum',
 'flow.p': 'Ein klarer, nachvollziehbarer Weg von der Anfrage bis zur Inbetriebnahme — betreut durch unser Export-Engineering-Team.',
 'flow.s1t': 'Anfrage & technisches Angebot', 'flow.s1d': 'Senden Sie Spannung, Last und Anordnung — maßgeschneiderte Kabelkonfiguration und Werksangebot innerhalb von 24 Stunden.',
 'flow.s2t': 'Vertrag & Produktionsplan', 'flow.s2d': 'Bestätigte Bestellung kommt in den Produktionsplan mit vereinbartem Lieferfenster.',
 'flow.s3t': 'Fertigung & vollständige Prüfung', 'flow.s3d': 'Produktion auf eigenen Linien; jede Trommel vor Freigabe 100% werksgeprüft.',
 'flow.s4t': 'Exportdokumentation', 'flow.s4d': 'Vollständige Exportunterlagen: Zertifikate, Packlisten, Zoll- und EAC/CE-Dokumente.',
 'flow.s5t': 'Pünktliche Lieferung & Support', 'flow.s5d': 'Bahn, Straße oder See bis zum Standort — mit Anleitungen zu Muffen, Endverschlüssen und Verlegung.',
 'serve.title': 'KI-Infrastrukturprojekte weltweit',
 'serve.p': 'Exportabdeckung: Zentralasien · Naher Osten · Russland · Europa · Amerika, u. a. Usbekistan, Kasachstan, Türkei, Deutschland, Malaysia, Mexiko.',
 'serve.th1': 'Region', 'serve.th2': 'Kernmärkte', 'serve.th3': 'Was wir liefern',
 'serve.r1k': 'Zentralasien', 'serve.r1m': 'Usbekistan, Kasachstan, Mongolei', 'serve.r1s': 'GOST-zertifizierte Kabel, EAC-Dokumente, Bahn- und Straßentransport',
 'serve.r2k': 'Naher Osten', 'serve.r2m': 'VAE, Saudi-Arabien, Türkei', 'serve.r2s': 'IEC-zertifizierte Kabel für Rechenzentren und Smart-City-Projekte',
 'serve.r3k': 'Russland & GUS', 'serve.r3m': 'Russland, Ukraine, Belarus', 'serve.r3s': 'Kältebeständige Manteloptionen, EAC-Zertifizierung',
 'serve.r4k': 'Europa', 'serve.r4m': 'Deutschland, Frankreich, Spanien, Portugal', 'serve.r4s': 'IEC-60502-2-Kabel mit schneller See- und Bahnlogistik',
 'serve.r5k': 'Amerika', 'serve.r5m': 'USA, Mexiko, Brasilien', 'serve.r5s': 'Hochstromkabel, IEC-konforme Fertigung',
 'faq.title': 'FAQ — 35-kV-Rechenleistungskabel',
 'faq.q1': 'Wie lange ist die Lieferzeit?', 'faq.a1': 'Standardaufträge 35 kV: Versand in 3–5 Wochen je nach Umfang; Großprojekte planen wir nach Ihrem Bauzeitplan.',
 'faq.q2': 'Liefern Sie Exportdokumente und Zertifikate?', 'faq.a2': 'Ja — IEC-, GOST/EAC-Prüfzertifikate, Packlisten, Rechnungen und vollständige Zolldokumente bei jeder Lieferung.',
 'faq.q3': 'Wie hoch ist die Mindestbestellmenge?', 'faq.a3': 'Kein festes Minimum für Standardkonfigurationen — nennen Sie Ihren Bedarf, wir empfehlen wirtschaftliche Trommellängen.',
 'faq.q4': 'Kundenspezifische Querschnitte und Schirme?', 'faq.a4': 'Ja. Unser Werk unterstützt Sonderquerschnitte, Kupferschirme und Bewehrungen; senden Sie Ihre Spezifikation für ein kostenloses Angebot.',
 'faq.q5': 'Wie erhalte ich schnell einen Preis?', 'faq.a5': 'Senden Sie per E-Mail oder WhatsApp Spannung, Querschnitt, Länge und Menge — Richtpreis innerhalb eines Werktags.',
 'cta.title': 'Bereit, Ihr KI-Rechenzentrum zu versorgen?',
 'cta.p': 'Nennen Sie Standort, Spannung und Kabelanforderungen. Unsere Exportingenieure antworten innerhalb von 24 Stunden mit Lösung und Werkspreis.',
 'cta.email': 'E-Mail: info@ouzcable.com', 'cta.phone': 'Tel: +998 99 851 6999',
 'cta.whatsapp': 'WhatsApp: +998 99 851 6999', 'cta.telegram': 'Telegram: @H99G99',
 'contact.email': 'E-Mail:', 'contact.phone': 'Tel:', 'contact.whatsapp': 'WhatsApp:', 'contact.telegram': 'Telegram:',
 'contact.hq': 'Hauptsitz:', 'contact.hqval': 'China · Export weltweit', 'contact.web': 'Website:',
 'footer.back': '← Zurück zur OUZHI-Cable-Startseite', 'footer.rights': 'Alle Rechte vorbehalten.',
}

T['uk'] = {
 'hero.eyebrow': 'Кабелі для обчислень · ЦОД штучного інтелекту · 2026',
 'hero.title': 'Кабель 35 кВ для обчислювальних потужностей — <span class="accent">Енергія для ери ШІ</span>',
 'hero.sub': 'OUZHI Cable (欧智电缆) — завод-виробник кабелів 35 кВ для ЦОД штучного інтелекту',
 'hero.lead': 'GPU-кластери, стійки високої щільності та дата-центри мегаватного класу потребують надійного живлення середньої напруги. OUZHI Cable проєктує та виробляє кабелі 35 кВ для обчислювальних потужностей — ізоляція XLPE, мідна жила, вогнестійка оболонка LSZH — на власному заводі в Китаї, з доставкою в дата-центри по всьому світу.',
 'hero.cta1': 'Отримати ціну заводу', 'hero.cta2': 'Технічні параметри',
 'why.title': 'Чому потрібен спеціальний кабель для обчислень?',
 'why.p': 'Дата-центри ШІ — вже не звичайні будівлі, а споживачі мегаватного масштабу. Кабель середньої напруги, що їх живить, має поєднувати високу струмову здатність, пожежну безпеку та довговічність.',
 'why.c1t': 'Передача потужності високої щільності', 'why.c1d': 'Одножильні кабелі 26/35 кВ XLPE передають мегаватні навантаження від підстанції до трансформаторів ШІ-кластерів із мінімальними втратами.',
 'why.c2t': 'Пожежобезпечна конструкція LSZH', 'why.c2d': 'Оболонка LSZH обмежує токсичний дим і корозійні гази в закритих залах — захищає людей, сервери та безперервність бізнесу.',
 'why.c3t': 'Сертифікація за світовими стандартами', 'why.c3d': 'Виробництво та 100% заводський контроль за IEC 60502-2, GOST 31996 та GB/T 12706 — визнано енергокомпаніями та EPC-підрядниками.',
 'why.c4t': 'Швидкість і ціна заводу-виробника', 'why.c4d': 'Власні лінії — короткі терміни, індивідуальні довжини барабанів і конкурентні ціни — без посередників.',
 'spec.title': 'Кабель 35 кВ для обчислень — технічні характеристики',
 'spec.p': 'Нижче стандартні конфігурації; перерізи, довжини та екрани — на замовлення.',
 'spec.k1': 'Номінальна напруга', 'spec.v1': '26/35 кВ (також 12/20 кВ, 18/30 кВ)',
 'spec.k2': 'Жила', 'spec.v2': 'Мідь (Cu) або алюміній (Al), клас 2',
 'spec.k3': 'Ізоляція', 'spec.v3': 'XLPE (зшитий поліетилен), потрійна екструзія',
 'spec.k4': 'Екран', 'spec.v4': 'Мідний дротовий / стрічковий екран',
 'spec.k5': 'Броня', 'spec.v5': 'Сталева дротова броня SWA (опційно)',
 'spec.k6': 'Оболонка', 'spec.v6': 'LSZH вогнестійка, безгалогенна',
 'spec.k7': 'Стандарти', 'spec.v7': 'IEC 60502-2 · GOST 31996 · GB/T 12706',
 'spec.k8': 'Застосування', 'spec.v8': 'Дата-центри ШІ, обчислювальні центри, живлення підстанцій, приміщення ІБП',
 'flow.title': 'Від нашого заводу до вашого дата-центру',
 'flow.p': 'Прозорий шлях від запиту до введення в експлуатацію — під управлінням нашої експортної інженерної команди.',
 'flow.s1t': 'Запит і технічна пропозиція', 'flow.s1d': 'Вкажіть напругу, навантаження та схему — конфігурація кабелю та ціна заводу протягом 24 годин.',
 'flow.s2t': 'Контракт і план виробництва', 'flow.s2d': 'Підтверджене замовлення входить у графік виробництва з узгодженим терміном.',
 'flow.s3t': 'Виробництво та повний контроль', 'flow.s3d': 'Випуск на власних лініях; кожен барабан 100% перевірено перед відвантаженням.',
 'flow.s4t': 'Експортна документація', 'flow.s4d': 'Повний пакет: сертифікати, пакувальні листи, митні та EAC/CE документи.',
 'flow.s5t': 'Своєчасна поставка та підтримка', 'flow.s5d': 'Залізниця, авто або море до об\u2019єкта — з рекомендаціями з монтажу та оконцювання.',
 'serve.title': 'Обслуговування проєктів ШІ-інфраструктури по всьому світу',
 'serve.p': 'Експорт у Центральну Азію · Близький Схід · Росію · Європу · Америку, включаючи Узбекистан, Казахстан, Туреччину, Німеччину, Малайзію, Мексику та ін.',
 'serve.th1': 'Регіон', 'serve.th2': 'Ключові ринки', 'serve.th3': 'Що ми постачаємо',
 'serve.r1k': 'Центральна Азія', 'serve.r1m': 'Узбекистан, Казахстан, Монголія', 'serve.r1s': 'Кабелі з сертифікатами ГОСТ, документи EAC, доставка залізницею та авто',
 'serve.r2k': 'Близький Схід', 'serve.r2m': 'ОАЕ, Саудівська Аравія, Туреччина', 'serve.r2s': 'Кабелі IEC для дата-центрів і розумних міст',
 'serve.r3k': 'Росія та СНД', 'serve.r3m': 'Росія, Україна, Білорусь', 'serve.r3s': 'Холодостійкі оболонки, сертифікація EAC',
 'serve.r4k': 'Європа', 'serve.r4m': 'Німеччина, Франція, Іспанія, Португалія', 'serve.r4s': 'Кабелі IEC 60502-2, швидка морська та залізнична логістика',
 'serve.r5k': 'Америка', 'serve.r5m': 'США, Мексика, Бразилія', 'serve.r5s': 'Кабелі з високою струмовою здатністю, виробництво за IEC',
 'faq.title': 'Питання та відповіді — кабель 35 кВ для обчислень',
 'faq.q1': 'Який термін поставки?', 'faq.a1': 'Стандартні замовлення 35 кВ відвантажуються за 3–5 тижнів залежно від обсягу; великі проєкти узгоджуємо з графіком будівництва.',
 'faq.q2': 'Чи надаєте експортні документи та сертифікати?', 'faq.a2': 'Так — сертифікати IEC, GOST/EAC, пакувальні листи, інвойси та повна митна документація додаються до кожної поставки.',
 'faq.q3': 'Який мінімальний обсяг замовлення?', 'faq.a3': 'Для стандартних конфігурацій фіксованого мінімуму немає — вкажіть потреби проєкту, запропонуємо економні довжини.',
 'faq.q4': 'Чи можливі нестандартні перерізи та екрани?', 'faq.a4': 'Так. Завод підтримує індивідуальні перерізи, мідні екрани та броню; надішліть специфікацію — отримаєте безкоштовну пропозицію.',
 'faq.q5': 'Як швидко отримати ціну?', 'faq.a5': 'Надішліть email або WhatsApp напругу, переріз, довжину та кількість — орієнтовна ціна протягом одного робочого дня.',
 'cta.title': 'Готові забезпечити енергією ваш дата-центр ШІ?',
 'cta.p': 'Повідомте локацію проєкту, напругу та вимоги до кабелю. Експортні інженери відповідають протягом 24 годин з рішенням і ціною заводу.',
 'cta.email': 'Email: info@ouzcable.com', 'cta.phone': 'Тел: +998 99 851 6999',
 'cta.whatsapp': 'WhatsApp: +998 99 851 6999', 'cta.telegram': 'Telegram: @H99G99',
 'contact.email': 'Email:', 'contact.phone': 'Тел:', 'contact.whatsapp': 'WhatsApp:', 'contact.telegram': 'Telegram:',
 'contact.hq': 'Головний офіс:', 'contact.hqval': 'Китай · Експорт у всьому світі', 'contact.web': 'Сайт:',
 'footer.back': '← На головну OUZHI Cable', 'footer.rights': 'Усі права захищено.',
}

T['es'] = {
 'hero.eyebrow': 'Cable de cómputo · Centros de datos IA · 2026',
 'hero.title': 'Cable de 35 kV para potencia de cómputo — <span class="accent">Energía para la era de la IA</span>',
 'hero.sub': 'OUZHI Cable (欧智电缆) — fábrica de origen de cables de 35 kV para centros de datos IA',
 'hero.lead': 'Los clústeres de GPU, racks de alta densidad y salas de datos a escala de megavatios exigen energía de media tensión fiable. OUZHI Cable diseña y fabrica cables de potencia de cómputo de 35 kV — aislamiento XLPE, conductor de cobre, cubierta LSZH ignífuga — en nuestra fábrica de origen en China, entregados en todo el mundo.',
 'hero.cta1': 'Obtener precio de fábrica', 'hero.cta2': 'Ver especificaciones',
 'why.title': '¿Por qué un cable dedicado a potencia de cómputo?',
 'why.p': 'Los centros de datos de IA ya no son edificios comunes — son consumidores a escala de megavatios. El cable de media tensión que los alimenta debe combinar alta ampacidad, seguridad contra incendios y fiabilidad a largo plazo.',
 'why.c1t': 'Entrega de energía de alta densidad', 'why.c1d': 'Los cables unipolares 26/35 kV XLPE transportan cargas de MW de la subestación a los transformadores de clústeres IA con mínimas pérdidas.',
 'why.c2t': 'Construcción LSZH ignífuga', 'why.c2d': 'La cubierta LSZH limita humo tóxico y gases corrosivos en salas cerradas — protegiendo personas, servidores y continuidad del negocio.',
 'why.c3t': 'Certificado según normas globales', 'why.c3d': 'Fabricado y probado 100% en fábrica según IEC 60502-2, GOST 31996 y GB/T 12706 — aceptado por utilities y contratistas EPC.',
 'why.c4t': 'Velocidad y precio de fábrica', 'why.c4d': 'Líneas propias: plazos cortos, longitudes de bobina personalizadas y precios competitivos — sin intermediarios.',
 'spec.title': 'Cable 35 kV para cómputo — especificaciones técnicas',
 'spec.p': 'Configuraciones estándar abajo; secciones, longitudes y pantallas a pedido.',
 'spec.k1': 'Tensión nominal', 'spec.v1': '26/35 kV (también 12/20 kV, 18/30 kV)',
 'spec.k2': 'Conductor', 'spec.v2': 'Cobre (Cu) o aluminio (Al), clase 2',
 'spec.k3': 'Aislamiento', 'spec.v3': 'XLPE (polietileno reticulado), triple extrusión',
 'spec.k4': 'Pantalla', 'spec.v4': 'Pantalla metálica de alambre/cinta de cobre',
 'spec.k5': 'Armadura', 'spec.v5': 'Armadura de alambre de acero SWA (opcional)',
 'spec.k6': 'Cubierta', 'spec.v6': 'LSZH ignífuga, sin halógenos',
 'spec.k7': 'Normas', 'spec.v7': 'IEC 60502-2 · GOST 31996 · GB/T 12706',
 'spec.k8': 'Aplicación', 'spec.v8': 'Centros de datos IA, hubs de cómputo, alimentación de subestaciones, salas UPS',
 'flow.title': 'De nuestra fábrica a su centro de datos',
 'flow.p': 'Un camino claro y trazable, de la consulta a la puesta en servicio — gestionado por nuestro equipo de ingeniería de exportación.',
 'flow.s1t': 'Consulta y propuesta técnica', 'flow.s1d': 'Envíe tensión, carga y layout — configuración a medida y precio de fábrica en 24 horas.',
 'flow.s2t': 'Contrato y plan de producción', 'flow.s2d': 'El pedido confirmado entra en el calendario con una ventana de entrega acordada.',
 'flow.s3t': 'Fabricación y pruebas completas', 'flow.s3d': 'Producido en nuestras líneas; cada bobina 100% probada antes de su liberación.',
 'flow.s4t': 'Documentación de exportación', 'flow.s4d': 'Paquete completo: certificados, listas de empaque, aduanas y documentos EAC/CE.',
 'flow.s5t': 'Entrega puntual y soporte', 'flow.s5d': 'Ferrocarril, carretera o mar hasta su sitio — con guía de empalmes, terminaciones e instalación.',
 'serve.title': 'Sirviendo proyectos de infraestructura IA en todo el mundo',
 'serve.p': 'Cobertura de exportación: Asia Central · Medio Oriente · Rusia · Europa · Américas, incluidos Uzbekistán, Kazajistán, Turquía, Alemania, Malasia, México y más.',
 'serve.th1': 'Región', 'serve.th2': 'Mercados clave', 'serve.th3': 'Lo que entregamos',
 'serve.r1k': 'Asia Central', 'serve.r1m': 'Uzbekistán, Kazajistán, Mongolia', 'serve.r1s': 'Cables certificados GOST, documentos EAC, entrega ferroviaria y por carretera',
 'serve.r2k': 'Medio Oriente', 'serve.r2m': 'EAU, Arabia Saudita, Turquía', 'serve.r2s': 'Cables certificados IEC para centros de datos y ciudades inteligentes',
 'serve.r3k': 'Rusia y CEI', 'serve.r3m': 'Rusia, Ucrania, Bielorrusia', 'serve.r3s': 'Opciones de cubierta resistente al frío, certificación EAC',
 'serve.r4k': 'Europa', 'serve.r4m': 'Alemania, Francia, España, Portugal', 'serve.r4s': 'Cables IEC 60502-2 con logística marítima y ferroviaria rápida',
 'serve.r5k': 'Américas', 'serve.r5m': 'EE. UU., México, Brasil', 'serve.r5s': 'Cables de alta ampacidad, fabricación conforme a IEC',
 'faq.title': 'FAQ — cable 35 kV para cómputo',
 'faq.q1': '¿Cuál es el plazo de entrega?', 'faq.a1': 'Pedidos estándar 35 kV: envío en 3–5 semanas según volumen; grandes proyectos se programan según su cronograma.',
 'faq.q2': '¿Proporcionan documentación de exportación y certificaciones?', 'faq.a2': 'Sí — certificados IEC, GOST/EAC, listas de empaque, facturas y documentación aduanera completa en cada envío.',
 'faq.q3': '¿Cuál es la cantidad mínima de pedido?', 'faq.a3': 'Sin mínimo fijo para configuraciones estándar — díganos sus necesidades y recomendaremos longitudes económicas.',
 'faq.q4': '¿Pueden suministrar secciones y pantallas personalizadas?', 'faq.a4': 'Sí. Nuestra fábrica soporta secciones, pantallas de cobre y armaduras a medida; envíe su especificación para una propuesta gratuita.',
 'faq.q5': '¿Cómo obtengo un precio rápido?', 'faq.a5': 'Envíe por correo o WhatsApp tensión, sección, longitud y cantidad — precio indicativo en un día hábil.',
 'cta.title': '¿Listo para alimentar su centro de datos IA?',
 'cta.p': 'Cuéntenos ubicación, tensión y requisitos del cable. Nuestros ingenieros de exportación responden en 24 horas con solución a medida y precio de fábrica.',
 'cta.email': 'Email: info@ouzcable.com', 'cta.phone': 'Tel: +998 99 851 6999',
 'cta.whatsapp': 'WhatsApp: +998 99 851 6999', 'cta.telegram': 'Telegram: @H99G99',
 'contact.email': 'Email:', 'contact.phone': 'Tel:', 'contact.whatsapp': 'WhatsApp:', 'contact.telegram': 'Telegram:',
 'contact.hq': 'Sede:', 'contact.hqval': 'China · Exportación mundial', 'contact.web': 'Sitio web:',
 'footer.back': '← Volver al inicio de OUZHI Cable', 'footer.rights': 'Todos los derechos reservados.',
}

T['tr'] = {
 'hero.eyebrow': 'Hesaplama Gücü Kablosu · Yapay Zeka Veri Merkezleri · 2026',
 'hero.title': '35 kV Hesaplama Gücü Kablosu — <span class="accent">Yapay Zeka Çağına Güç</span>',
 'hero.sub': 'OUZHI Cable (欧智电缆) — Yapay Zeka Veri Merkezleri için 35 kV Kablo Kaynak Fabrikası',
 'hero.lead': 'GPU kümeleri, yüksek yoğunluklu raflar ve megavat ölçeğindeki veri salonları güvenilir orta gerilim gücü gerektirir. OUZHI Cable, Çin\u2019deki kendi kaynak fabrikamızda 35 kV hesaplama gücü kabloları tasarlar ve üretir — XLPE izolasyon, bakır iletken, LSZH yangın güvenli kılıf — dünya genelindeki veri merkezlerine teslim edilir.',
 'hero.cta1': 'Fabrika Fiyatı Alın', 'hero.cta2': 'Teknik Özellikler',
 'why.title': 'Neden Özel Bir Hesaplama Gücü Kablosu?',
 'why.p': 'Yapay zeka veri merkezleri artık sıradan binalar değil — megavat ölçeğinde enerji tüketicileri. Onları besleyen orta gerilim kablosu yüksek akım taşıma, yangın güvenliği ve uzun vadeli güvenilirliği birleştirmelidir.',
 'why.c1t': 'Yüksek Yoğunluklu Güç İletimi', 'why.c1d': 'Tek damarlı 26/35 kV XLPE kablolar, MW ölçeğindeki yükleri trafo merkezinden yapay zeka kümesi transformatörlerine minimum kayıpla taşır.',
 'why.c2t': 'Yangın Güvenli LSZH Yapı', 'why.c2d': 'LSZH kılıf, kapalı veri salonlarında zehirli dumanı ve korozif gazları sınırlar — insanları, sunucuları ve iş sürekliliğini korur.',
 'why.c3t': 'Küresel Standartlara Uygun Sertifikalı', 'why.c3d': 'IEC 60502-2, GOST 31996 ve GB/T 12706\u2019ya göre üretilir ve %100 fabrika testinden geçer — kurumlar ve EPC yüklenicileri tarafından kabul edilir.',
 'why.c4t': 'Fabrika Doğrudan Hız ve Fiyat', 'why.c4d': 'Kendi üretim hatları: kısa teslim süreleri, özel makara uzunlukları ve rekabetçi fabrika fiyatları — aracısız.',
 'spec.title': '35 kV Hesaplama Gücü Kablosu — Teknik Özellikler',
 'spec.p': 'Aşağıda standart konfigürasyonlar; kesit, uzunluk ve ekranlar talep üzerine.',
 'spec.k1': 'Anma gerilimi', 'spec.v1': '26/35 kV (ayrıca 12/20 kV, 18/30 kV)',
 'spec.k2': 'İletken', 'spec.v2': 'Bakır (Cu) veya alüminyum (Al), sınıf 2',
 'spec.k3': 'İzolasyon', 'spec.v3': 'XLPE (çapraz bağlı polietilen), üçlü ekstrüzyon',
 'spec.k4': 'Ekran', 'spec.v4': 'Bakır tel / şerit metal ekran',
 'spec.k5': 'Zırh', 'spec.v5': 'SWA çelik tel zırh (opsiyonel)',
 'spec.k6': 'Kılıf', 'spec.v6': 'LSZH alev geciktirici, halojensiz',
 'spec.k7': 'Standartlar', 'spec.v7': 'IEC 60502-2 · GOST 31996 · GB/T 12706',
 'spec.k8': 'Uygulama', 'spec.v8': 'Yapay zeka veri merkezleri, hesaplama merkezleri, trafo beslemeleri, UPS odaları',
 'flow.title': 'Fabrikamızdan Veri Merkezinize',
 'flow.p': 'Talepten enerjilendirmeye net ve izlenebilir bir yol — ihracat mühendislik ekibimiz yönetir.',
 'flow.s1t': 'Talep ve Teknik Teklif', 'flow.s1d': 'Gerilim, yük ve yerleşimi gönderin — 24 saat içinde özel kablo konfigürasyonu ve fabrika fiyatı.',
 'flow.s2t': 'Sözleşme ve Üretim Planı', 'flow.s2d': 'Onaylanan sipariş, kararlaştırılan teslim penceresiyle üretim takvimine girer.',
 'flow.s3t': 'Üretim ve Tam Test', 'flow.s3d': 'Kendi hatlarımızda üretilir; her makara sevkiyattan önce %100 fabrika testinden geçer.',
 'flow.s4t': 'İhracat Dokümantasyonu', 'flow.s4d': 'Eksiksiz ihracat paketi: sertifikalar, paketleme listeleri, gümrük ve EAC/CE belgeleri.',
 'flow.s5t': 'Zamanında Teslimat ve Destek', 'flow.s5d': 'Demiryolu, kara veya deniz ile sahanıza — ek, sonlandırma ve döşeme rehberliğiyle.',
 'serve.title': 'Dünya Genelinde Yapay Zeka Altyapı Projelerine Hizmet',
 'serve.p': 'İhracat kapsamı: Orta Asya · Orta Doğu · Rusya · Avrupa · Amerika — Özbekistan, Kazakistan, Türkiye, Almanya, Malezya, Meksika ve daha fazlası.',
 'serve.th1': 'Bölge', 'serve.th2': 'Kilit Pazarlar', 'serve.th3': 'Teslim Ettiklerimiz',
 'serve.r1k': 'Orta Asya', 'serve.r1m': 'Özbekistan, Kazakistan, Moğolistan', 'serve.r1s': 'GOST sertifikalı kablolar, EAC belgeleri, demiryolu ve kara teslimat',
 'serve.r2k': 'Orta Doğu', 'serve.r2m': 'BAE, Suudi Arabistan, Türkiye', 'serve.r2s': 'Veri merkezleri ve akıllı şehirler için IEC sertifikalı kablolar',
 'serve.r3k': 'Rusya ve BDT', 'serve.r3m': 'Rusya, Ukrayna, Beyaz Rusya', 'serve.r3s': 'Soğuğa dayanıklı kılıf seçenekleri, EAC sertifikasyonu',
 'serve.r4k': 'Avrupa', 'serve.r4m': 'Almanya, Fransa, İspanya, Portekiz', 'serve.r4s': 'IEC 60502-2 kablolar, hızlı deniz ve demiryolu lojistiği',
 'serve.r5k': 'Amerika', 'serve.r5m': 'ABD, Meksika, Brezilya', 'serve.r5s': 'Yüksek ampasiteli besleme kabloları, IEC uyumlu üretim',
 'faq.title': 'SSS — 35 kV Hesaplama Gücü Kablosu',
 'faq.q1': 'Teslim süresi nedir?', 'faq.a1': 'Standart 35 kV siparişleri hacme bağlı olarak 3–5 haftada sevk edilir; büyük projeler inşaat takviminize göre planlanır.',
 'faq.q2': 'İhracat belgeleri ve sertifikalar sağlıyor musunuz?', 'faq.a2': 'Evet — IEC, GOST/EAC test sertifikaları, paketleme listeleri, faturalar ve tam gümrük belgeleri her sevkiyata dahildir.',
 'faq.q3': 'Minimum sipariş miktarı nedir?', 'faq.a3': 'Standart konfigürasyonlar için sabit minimum yoktur — proje ihtiyaçlarınızı söyleyin, en ekonomik makara uzunluklarını önerelim.',
 'faq.q4': 'Özel kesit ve ekran sağlayabilir misiniz?', 'faq.a4': 'Evet. Fabrikamız özel kesitler, bakır ekranlar ve zırh seçenekleri destekler; ücretsiz teklif için spesifikasyonunuzu gönderin.',
 'faq.q5': 'Hızlı fiyat nasıl alırım?', 'faq.a5': 'E-posta veya WhatsApp ile gerilim, kesit, uzunluk ve miktarı gönderin — bir iş günü içinde gösterge fiyat.',
 'cta.title': 'Yapay Zeka Veri Merkezinize Güç Vermeye Hazır mısınız?',
 'cta.p': 'Proje konumunuzu, gerilimi ve kablo gereksinimlerinizi iletin. İhracat mühendislerimiz 24 saat içinde özel çözüm ve fabrika fiyatıyla yanıtlar.',
 'cta.email': 'E-posta: info@ouzcable.com', 'cta.phone': 'Tel: +998 99 851 6999',
 'cta.whatsapp': 'WhatsApp: +998 99 851 6999', 'cta.telegram': 'Telegram: @H99G99',
 'contact.email': 'E-posta:', 'contact.phone': 'Tel:', 'contact.whatsapp': 'WhatsApp:', 'contact.telegram': 'Telegram:',
 'contact.hq': 'Merkez:', 'contact.hqval': 'Çin · Dünya genelinde ihracat', 'contact.web': 'Web sitesi:',
 'footer.back': '← OUZHI Cable ana sayfasına dön', 'footer.rights': 'Tüm hakları saklıdır.',
}

T['pt'] = {
 'hero.eyebrow': 'Cabo de potência de computação · Data centers de IA · 2026',
 'hero.title': 'Cabo de 35 kV para potência de computação — <span class="accent">Energia para a era da IA</span>',
 'hero.sub': 'OUZHI Cable (欧智电缆) — fábrica de origem de cabos de 35 kV para data centers de IA',
 'hero.lead': 'Clusters de GPU, racks de alta densidade e salas de dados em escala de megawatts exigem energia de média tensão confiável. A OUZHI Cable projeta e fabrica cabos de potência de computação de 35 kV — isolação XLPE, condutor de cobre, cobertura LSZH ignífuga — em nossa fábrica de origem na China, entregues em todo o mundo.',
 'hero.cta1': 'Obter preço de fábrica', 'hero.cta2': 'Ver especificações',
 'why.title': 'Por que um cabo dedicado à potência de computação?',
 'why.p': 'Data centers de IA não são mais edifícios comuns — são consumidores em escala de megawatts. O cabo de média tensão que os alimenta deve combinar alta ampacidade, segurança contra incêndio e confiabilidade de longo prazo.',
 'why.c1t': 'Entrega de energia de alta densidade', 'why.c1d': 'Cabos unipolares 26/35 kV XLPE transportam cargas de MW da subestação aos transformadores de clusters de IA com perdas mínimas.',
 'why.c2t': 'Construção LSZH ignífuga', 'why.c2d': 'A cobertura LSZH limita fumaça tóxica e gases corrosivos em salas fechadas — protegendo pessoas, servidores e continuidade dos negócios.',
 'why.c3t': 'Certificado conforme normas globais', 'why.c3d': 'Fabricado e testado 100% em fábrica conforme IEC 60502-2, GOST 31996 e GB/T 12706 — aceito por utilities e contratantes EPC.',
 'why.c4t': 'Velocidade e preço de fábrica', 'why.c4d': 'Linhas próprias: prazos curtos, comprimentos de bobina personalizados e preços competitivos — sem intermediários.',
 'spec.title': 'Cabo 35 kV para computação — especificações técnicas',
 'spec.p': 'Configurações padrão abaixo; seções, comprimentos e telas sob consulta.',
 'spec.k1': 'Tensão nominal', 'spec.v1': '26/35 kV (também 12/20 kV, 18/30 kV)',
 'spec.k2': 'Condutor', 'spec.v2': 'Cobre (Cu) ou alumínio (Al), classe 2',
 'spec.k3': 'Isolação', 'spec.v3': 'XLPE (polietileno reticulado), tripla extrusão',
 'spec.k4': 'Tela', 'spec.v4': 'Tela metálica de fio/fita de cobre',
 'spec.k5': 'Armadura', 'spec.v5': 'Armadura de fio de aço SWA (opcional)',
 'spec.k6': 'Cobertura', 'spec.v6': 'LSZH ignífuga, sem halogênios',
 'spec.k7': 'Normas', 'spec.v7': 'IEC 60502-2 · GOST 31996 · GB/T 12706',
 'spec.k8': 'Aplicação', 'spec.v8': 'Data centers de IA, hubs de computação, alimentação de subestações, salas de UPS',
 'flow.title': 'Da nossa fábrica ao seu data center',
 'flow.p': 'Um caminho claro e rastreável, da consulta à energização — gerenciado pela nossa equipe de engenharia de exportação.',
 'flow.s1t': 'Consulta e proposta técnica', 'flow.s1d': 'Envie tensão, carga e layout — configuração personalizada e preço de fábrica em 24 horas.',
 'flow.s2t': 'Contrato e plano de produção', 'flow.s2d': 'O pedido confirmado entra no cronograma com janela de entrega acordada.',
 'flow.s3t': 'Fabricação e testes completos', 'flow.s3d': 'Produzido em nossas linhas; cada bobina 100% testada antes da liberação.',
 'flow.s4t': 'Documentação de exportação', 'flow.s4d': 'Pacote completo: certificados, listas de embalagem, alfândega e documentos EAC/CE.',
 'flow.s5t': 'Entrega pontual e suporte', 'flow.s5d': 'Ferrovia, rodovia ou mar até o seu local — com orientação de emendas, terminações e instalação.',
 'serve.title': 'Atendendo projetos de infraestrutura de IA no mundo todo',
 'serve.p': 'Cobertura de exportação: Ásia Central · Oriente Médio · Rússia · Europa · Américas, incluindo Uzbequistão, Cazaquistão, Turquia, Alemanha, Malásia, México e mais.',
 'serve.th1': 'Região', 'serve.th2': 'Mercados-chave', 'serve.th3': 'O que entregamos',
 'serve.r1k': 'Ásia Central', 'serve.r1m': 'Uzbequistão, Cazaquistão, Mongólia', 'serve.r1s': 'Cabos certificados GOST, documentos EAC, entrega ferroviária e rodoviária',
 'serve.r2k': 'Oriente Médio', 'serve.r2m': 'EAU, Arábia Saudita, Turquia', 'serve.r2s': 'Cabos certificados IEC para data centers e cidades inteligentes',
 'serve.r3k': 'Rússia e CEI', 'serve.r3m': 'Rússia, Ucrânia, Bielorrússia', 'serve.r3s': 'Opções de cobertura resistente ao frio, certificação EAC',
 'serve.r4k': 'Europa', 'serve.r4m': 'Alemanha, França, Espanha, Portugal', 'serve.r4s': 'Cabos IEC 60502-2 com logística marítima e ferroviária rápida',
 'serve.r5k': 'Américas', 'serve.r5m': 'EUA, México, Brasil', 'serve.r5s': 'Cabos de alta ampacidade, fabricação conforme IEC',
 'faq.title': 'FAQ — cabo 35 kV para computação',
 'faq.q1': 'Qual o prazo de entrega?', 'faq.a1': 'Pedidos padrão 35 kV: envio em 3–5 semanas conforme volume; grandes projetos são programados conforme seu cronograma.',
 'faq.q2': 'Vocês fornecem documentação de exportação e certificações?', 'faq.a2': 'Sim — certificados IEC, GOST/EAC, listas de embalagem, faturas e documentação alfandegária completa em cada envio.',
 'faq.q3': 'Qual a quantidade mínima de pedido?', 'faq.a3': 'Sem mínimo fixo para configurações padrão — diga suas necessidades e recomendaremos comprimentos econômicos.',
 'faq.q4': 'Vocês fornecem seções e telas personalizadas?', 'faq.a4': 'Sim. Nossa fábrica suporta seções, telas de cobre e armaduras personalizadas; envie sua especificação para proposta gratuita.',
 'faq.q5': 'Como obter um preço rápido?', 'faq.a5': 'Envie por e-mail ou WhatsApp tensão, seção, comprimento e quantidade — preço indicativo em um dia útil.',
 'cta.title': 'Pronto para alimentar seu data center de IA?',
 'cta.p': 'Informe localização, tensão e requisitos do cabo. Nossos engenheiros de exportação respondem em 24 horas com solução personalizada e preço de fábrica.',
 'cta.email': 'E-mail: info@ouzcable.com', 'cta.phone': 'Tel: +998 99 851 6999',
 'cta.whatsapp': 'WhatsApp: +998 99 851 6999', 'cta.telegram': 'Telegram: @H99G99',
 'contact.email': 'E-mail:', 'contact.phone': 'Tel:', 'contact.whatsapp': 'WhatsApp:', 'contact.telegram': 'Telegram:',
 'contact.hq': 'Sede:', 'contact.hqval': 'China · Exportação mundial', 'contact.web': 'Site:',
 'footer.back': '← Voltar ao início da OUZHI Cable', 'footer.rights': 'Todos os direitos reservados.',
}

T['mn'] = {
 'hero.eyebrow': 'Тооцооллын хүчдэлийн кабел · AI өгөгдлийн төв · 2026',
 'hero.title': '35 кВ тооцооллын кабел — <span class="accent">AI эриний эрчим хүч</span>',
 'hero.sub': 'OUZHI Cable (欧智电缆) — AI өгөгдлийн төвийн 35 кВ кабелийн эх үүсвэр үйлдвэр',
 'hero.lead': 'GPU кластер, өндөр нягтралтай тавиур, мегаватт хэмжээний өгөгдлийн танхимууд найдвартай дундад хүчдэлийн тэжээл шаарддаг. OUZHI Cable нь Хятад дахь эх үүсвэр үйлдвэртээ 35 кВ тооцооллын кабелийг зохион бүтээж, үйлдвэрлэдэг — XLPE изоляц, мэс дамжуулагч, LSZH галд тэсвэртэй хүрдэл — дэлхийн өгөгдлийн төвүүдэд хүргэнэ.',
 'hero.cta1': 'Үйлдвэрийн үнэ авах', 'hero.cta2': 'Техникийн үзүүлэлт',
 'why.title': 'Яагаад тусгай тооцооллын кабел хэрэгтэй вэ?',
 'why.p': 'AI өгөгдлийн төвүүд энгийн барилга байхаа больсон — тэд мегаватт хэмжээний эрчим хүч хэрэглэгчид юм. Тэднийг тэжээх дундад хүчдэлийн кабел өндөр гүйдэл даах чадвар, гал аюулгүй байдал, урт хугацааны найдвартай байдлыг хослуулах ёстой.',
 'why.c1t': 'Өндөр нягтралтай эрчим хүч дамжуулалт', 'why.c1d': 'Нэг утастай 26/35 кВ XLPE кабел нь мегаватт ачааллыг дэд станцаас AI кластерын трансформаторт хамгийн бага алдагдалтай хүргэдэг.',
 'why.c2t': 'Галд тэсвэртэй LSZH бүтэц', 'why.c2d': 'LSZH хүрдэл нь хаалттай өгөгдлийн танхимд хорт утаа, зэврэлттэй хийг хязгаарладаг — хүмүүс, сервер, бизнесийн тасралтгүй байдлыг хамгаална.',
 'why.c3t': 'Олон улсын стандартаар гэрчилгээжсэн', 'why.c3d': 'IEC 60502-2, GOST 31996, GB/T 12706 стандартаар үйлдвэрлэж, 100% үйлдвэрийн шалгалт — эрчим хүчний компани, EPC гүржүүдээр хүлээн зөвшөөрөгдсөн.',
 'why.c4t': 'Үйлдвэрийн шууд хурд, үнэ', 'why.c4d': 'Өөрийн үйлдвэрлэлийн шугам: богино хугацаа, захиалгат ороомгийн урт, өрсөлдөхүйц үйлдвэрийн үнэ — зуучлагчгүйгээр.',
 'spec.title': '35 кВ тооцооллын кабел — техникийн үзүүлэлт',
 'spec.p': 'Доор стандарт тохиргоо; утасны хэмжээ, урт, дэлгэцийг захиалгаар хийнэ.',
 'spec.k1': 'Нэрлэсэн хүчдэл', 'spec.v1': '26/35 кВ (мөн 12/20 кВ, 18/30 кВ)',
 'spec.k2': 'Дамжуулагч', 'spec.v2': 'Мэс (Cu) эсвэл хөнгөн цагаан (Al), 2-р анги',
 'spec.k3': 'Изоляц', 'spec.v3': 'XLPE (хөндлөн холбоост полиэтилен), гурвалсан экструз',
 'spec.k4': 'Дэлгэц', 'spec.v4': 'Мэс утас / туузан металл дэлгэц',
 'spec.k5': 'Дэмжлэг', 'spec.v5': 'SWA ган утас дэмжлэг (нэмэлт)',
 'spec.k6': 'Хүрдэл', 'spec.v6': 'LSZH галд тэсвэртэй, галогенгүй',
 'spec.k7': 'Стандарт', 'spec.v7': 'IEC 60502-2 · GOST 31996 · GB/T 12706',
 'spec.k8': 'Хэрэглээ', 'spec.v8': 'AI өгөгдлийн төв, тооцооллын төв, дэд станцын тэжээл, UPS өрөө',
 'flow.title': 'Манай үйлдвэрээс таны өгөгдлийн төв хүртэл',
 'flow.p': 'Асуултаас эрчимжүүлэлт хүртэл тодорхой, хянах боломжтой зам — манай экспортын инженер баг удирдана.',
 'flow.s1t': 'Асуулт ба техникийн санал', 'flow.s1d': 'Хүчдэл, ачаалал, зохион байгуулалтаа илгээнэ үү — 24 цагийн дотор тохируулсан кабель, үйлдвэрийн үнэ.',
 'flow.s2t': 'Гэрээ ба үйлдвэрлэлийн төлөвлөгөө', 'flow.s2d': 'Баталгаажсан захиалга тохирсон хугацаатай үйлдвэрлэлийн хуваарьт орно.',
 'flow.s3t': 'Үйлдвэрлэл ба бүрэн шалгалт', 'flow.s3d': 'Өөрийн шугам дээр үйлдвэрлэж, гаргахаас өмнө ороомог бүр 100% шалгагдана.',
 'flow.s4t': 'Экспортын баримт бичиг', 'flow.s4d': 'Бүрэн экспортын багц: гэрчилгээ, савлалтын жагсаалт, гааль, EAC/CE баримт.',
 'flow.s5t': 'Цаг хугацаанд нь хүргэлт ба дэмжлэг', 'flow.s5d': 'Төмөр зам, авто эсвэл далайгаар — холболт, төгсгөл, суурилуулалтын зөвлөгөөтэй.',
 'serve.title': 'Дэлхий даяар AI дэд бүтцийн төслүүдэд үйлчилнэ',
 'serve.p': 'Экспортын хамрах хүрээ: Төв Ази · Ойрхи Дорнод · Орос · Европ · Америк — Узбекистан, Казахстан, Турк, Герман, Малайз, Мексик зэрэг.',
 'serve.th1': 'Бүс нутаг', 'serve.th2': 'Гол зах зээл', 'serve.th3': 'Бидний хүргэлт',
 'serve.r1k': 'Төв Ази', 'serve.r1m': 'Узбекистан, Казахстан, Монгол', 'serve.r1s': 'GOST гэрчилгээтэй кабел, EAC баримт, төмөр зам ба авто хүргэлт',
 'serve.r2k': 'Ойрхи Дорнод', 'serve.r2m': 'Арабын Нэгдсэн Эмират, Саудын Араб, Турк', 'serve.r2s': 'Өгөгдлийн төв, ухаалаг хотын төсөлд IEC гэрчилгээтэй кабел',
 'serve.r3k': 'Орос ба ТУХН', 'serve.r3m': 'Орос, Украйн, Беларусь', 'serve.r3s': 'Хүйтэнд тэсвэртэй хүрдэл, EAC гэрчилгээ',
 'serve.r4k': 'Европ', 'serve.r4m': 'Герман, Франц, Испани, Португал', 'serve.r4s': 'IEC 60502-2 кабел, хурдан далайн ба төмөр замын ложистик',
 'serve.r5k': 'Америк', 'serve.r5m': 'АНУ, Мексик, Бразил', 'serve.r5s': 'Өндөр гүйдлийн кабел, IEC-д нийцсэн үйлдвэрлэл',
 'faq.title': 'Түгээмэл асуулт — 35 кВ тооцооллын кабел',
 'faq.q1': 'Хүргэлтийн хугацаа хэд вэ?', 'faq.a1': 'Стандарт 35 кВ захиалгыг хэмжээнээс хамаарч 3–5 долоо хоногт ачуулна; том төслийг таны барилгын хуваарьтай зохицуулна.',
 'faq.q2': 'Экспортын баримт, гэрчилгээ өгдөг үү?', 'faq.a2': 'Тийм — IEC, GOST/EAC гэрчилгээ, савлалтын жагсаалт, нэхэмжлэх, бүрэн гаалийн баримт ачаа болгонд.',
 'faq.q3': 'Хамгийн бага захиалгын хэмжээ хэд вэ?', 'faq.a3': 'Стандарт тохиргоонд тогтмол доод хэмжээ байхгүй — төслийн хэрэгцээгээ хэлнэ үү, эдийн засгийн ороомгийн уртыг зөвлөнө.',
 'faq.q4': 'Захиалгат утасны хэмжээ, дэлгэц хийж чадах уу?', 'faq.a4': 'Тийм. Үйлдвэр захиалгат хэмжээ, мэс дэлгэц, дэмжлэгийн сонголтыг дэмждэг; үнэгүй санал авахын тулд үзүүлэлтээ илгээнэ үү.',
 'faq.q5': 'Хурдан үнийг хэрхэн авах вэ?', 'faq.a5': 'Имэйл эсвэл WhatsApp-аар хүчдэл, утас, урт, тоо хэмжээгээ илгээнэ үү — нэг ажлын өдөрт заагч үнэ.',
 'cta.title': 'AI өгөгдлийн төвдөө эрчим хүч өгөхөд бэлэн үү?',
 'cta.p': 'Төслийн байршил, хүчдэл, кабелийн шаардлагаа хэлнэ үү. Экспортын инженерүүд 24 цагийн дотор тохируулсан шийдэл, үйлдвэрийн шууд үнэтэй хариулах болно.',
 'cta.email': 'Имэйл: info@ouzcable.com', 'cta.phone': 'Утас: +998 99 851 6999',
 'cta.whatsapp': 'WhatsApp: +998 99 851 6999', 'cta.telegram': 'Telegram: @H99G99',
 'contact.email': 'Имэйл:', 'contact.phone': 'Утас:', 'contact.whatsapp': 'WhatsApp:', 'contact.telegram': 'Telegram:',
 'contact.hq': 'Төв:', 'contact.hqval': 'Хятад · Дэлхий даяар экспорт', 'contact.web': 'Вэб:',
 'footer.back': '← OUZHI Cable нүүр хуудас руу буцах', 'footer.rights': 'Бүх эрх хуулиар хамгаалагдсан.',
}

# ---- build body sections ----
def section(cls='section'):
    return f'<section class="{cls}">\n  <div class="container">\n'

body = ''
body += '''<section class="hero">
  <div class="container">
    <span class="eyebrow" data-i18n="hero.eyebrow">Computing Power Cable · AI Data Centers · 2026</span>
    <h1 data-i18n="hero.title">35 kV Computing Power Cable — <span class="accent">Powering the AI Era</span></h1>
    <div class="sub" data-i18n="hero.sub">OUZHI Cable (欧智电缆) — Source Factory for 35 kV AI Data Center Cables</div>
    <p class="lead" data-i18n="hero.lead">AI GPU clusters, high-density racks and megawatt-scale data halls demand reliable medium-voltage power. OUZHI Cable engineers and manufactures 35 kV computing power cables — XLPE insulation, copper conductor, LSZH fire-safe sheath — from our own source factory in China, delivered to data centers worldwide.</p>
    <div class="hero-cta">
      <a class="btn" href="#contact" data-i18n="hero.cta1">Get Factory Quote</a>
      <a class="btn btn-outline" href="https://ouzcable.com/technical.html" data-i18n="hero.cta2">View Technical Specs</a>
    </div>
  </div>
</section>
'''

body += section()
body += '''    <h2 data-i18n="why.title">Why a Dedicated Computing Power Cable?</h2>
    <p data-i18n="why.p">AI data centers are no longer ordinary buildings — they are megawatt-scale power consumers. The medium-voltage cable feeding them must combine high ampacity, fire safety and long-term reliability.</p>
    <div class="grid">
      <div class="card">
        <div class="num">01</div>
        <div class="t" data-i18n="why.c1t">High-Density Power Delivery</div>
        <div class="d" data-i18n="why.c1d">Single-core 26/35 kV XLPE cables carry MW-scale loads from substation to AI cluster transformers, minimizing losses on long data-center feeder runs.</div>
      </div>
      <div class="card">
        <div class="num">02</div>
        <div class="t" data-i18n="why.c2t">Fire-Safe LSZH Construction</div>
        <div class="d" data-i18n="why.c2d">Low-smoke, zero-halogen sheath limits toxic smoke and corrosive gas in enclosed data halls — protecting people, servers and business continuity.</div>
      </div>
      <div class="card">
        <div class="num">03</div>
        <div class="t" data-i18n="why.c3t">Certified to Global Standards</div>
        <div class="d" data-i18n="why.c3d">Manufactured and 100% factory-tested to IEC 60502-2, GOST 31996 and GB/T 12706 — accepted by utilities and EPC contractors across target markets.</div>
      </div>
      <div class="card">
        <div class="num">04</div>
        <div class="t" data-i18n="why.c4t">Factory-Direct Speed &amp; Price</div>
        <div class="d" data-i18n="why.c4d">Own production lines mean short lead times, custom drum lengths, and competitive factory pricing — no middlemen, no delays.</div>
      </div>
    </div>
  </div>
</section>
'''

body += section()
body += '''    <h2 data-i18n="spec.title">35 kV Computing Power Cable — Technical Specifications</h2>
    <p data-i18n="spec.p">Standard configurations below; custom conductor sizes, lengths and screens available on request.</p>
    <table>
      <tr><th data-i18n="spec.k1">Voltage rating</th><td data-i18n="spec.v1">26/35 kV (also 12/20 kV, 18/30 kV)</td></tr>
      <tr><th data-i18n="spec.k2">Conductor</th><td data-i18n="spec.v2">Copper (Cu) or aluminium (Al), class 2 stranded</td></tr>
      <tr><th data-i18n="spec.k3">Insulation</th><td data-i18n="spec.v3">XLPE (cross-linked polyethylene), triple-extrusion</td></tr>
      <tr><th data-i18n="spec.k4">Screen</th><td data-i18n="spec.v4">Copper wire / copper tape metallic screen</td></tr>
      <tr><th data-i18n="spec.k5">Armour</th><td data-i18n="spec.v5">SWA steel wire armouring (optional)</td></tr>
      <tr><th data-i18n="spec.k6">Sheath</th><td data-i18n="spec.v6">LSZH flame-retardant, low-smoke zero-halogen</td></tr>
      <tr><th data-i18n="spec.k7">Standards</th><td data-i18n="spec.v7">IEC 60502-2 · GOST 31996 · GB/T 12706</td></tr>
      <tr><th data-i18n="spec.k8">Application</th><td data-i18n="spec.v8">AI data centers, computing hubs, substation feeds, UPS rooms</td></tr>
    </table>
  </div>
</section>
'''

body += section()
body += '''    <h2 data-i18n="flow.title">From Our Factory to Your Data Center</h2>
    <p data-i18n="flow.p">A clear, trackable path from inquiry to energization — managed by our export engineering team.</p>
    <div class="steps">
      <div class="step"><div class="t" data-i18n="flow.s1t">Inquiry &amp; Technical Proposal</div><div class="d" data-i18n="flow.s1d">Send your voltage, load and layout — a tailored cable configuration and factory quote within 24 hours.</div></div>
      <div class="step"><div class="t" data-i18n="flow.s2t">Contract &amp; Production Plan</div><div class="d" data-i18n="flow.s2d">Confirmed order enters our production schedule with an agreed delivery window.</div></div>
      <div class="step"><div class="t" data-i18n="flow.s3t">Manufacturing &amp; Full Testing</div><div class="d" data-i18n="flow.s3d">Produced on our own lines; every drum 100% factory-tested before release.</div></div>
      <div class="step"><div class="t" data-i18n="flow.s4t">Export Documentation</div><div class="d" data-i18n="flow.s4d">Full export paperwork: certificates, packing lists, customs and EAC/CE documentation.</div></div>
      <div class="step"><div class="t" data-i18n="flow.s5t">On-Time Delivery &amp; Support</div><div class="d" data-i18n="flow.s5d">Rail, road or sea to your site — with jointing, termination and installation guidance.</div></div>
    </div>
  </div>
</section>
'''

body += section()
body += '''    <h2 data-i18n="serve.title">Serving AI Infrastructure Projects Worldwide</h2>
    <p data-i18n="serve.p">Export coverage across Central Asia · Middle East · Russia · Europe · Americas, including Uzbekistan, Kazakhstan, Turkey, Germany, Malaysia, Mexico and more.</p>
    <table>
      <tr><th data-i18n="serve.th1">Region</th><th data-i18n="serve.th2">Key Markets</th><th data-i18n="serve.th3">What We Deliver</th></tr>
      <tr><td data-i18n="serve.r1k">Central Asia</td><td data-i18n="serve.r1m">Uzbekistan, Kazakhstan, Mongolia</td><td data-i18n="serve.r1s">GOST-certified cables, EAC documents, rail &amp; road delivery to site</td></tr>
      <tr><td data-i18n="serve.r2k">Middle East</td><td data-i18n="serve.r2m">UAE, Saudi Arabia, Turkey</td><td data-i18n="serve.r2s">IEC-certified cables for data centers and smart-city projects</td></tr>
      <tr><td data-i18n="serve.r3k">Russia &amp; CIS</td><td data-i18n="serve.r3m">Russia, Ukraine, Belarus</td><td data-i18n="serve.r3s">Cold-resistant sheath options, EAC certification</td></tr>
      <tr><td data-i18n="serve.r4k">Europe</td><td data-i18n="serve.r4m">Germany, France, Spain, Portugal</td><td data-i18n="serve.r4s">IEC 60502-2 cables with fast sea and rail logistics</td></tr>
      <tr><td data-i18n="serve.r5k">Americas</td><td data-i18n="serve.r5m">USA, Mexico, Brazil</td><td data-i18n="serve.r5s">High-ampacity feeder cables, IEC-compliant manufacturing</td></tr>
    </table>
  </div>
</section>
'''

body += section()
body += '''    <h2 data-i18n="faq.title">FAQ — 35 kV Computing Power Cable</h2>
    <div class="faq-item">
      <div class="q" data-i18n="faq.q1">What lead time can I expect?</div>
      <div class="a" data-i18n="faq.a1">Standard 35 kV cable orders ship within 3–5 weeks depending on volume and configuration; large projects can be scheduled to match your construction timeline.</div>
    </div>
    <div class="faq-item">
      <div class="q" data-i18n="faq.q2">Do you provide export documentation and certifications?</div>
      <div class="a" data-i18n="faq.a2">Yes — IEC, GOST/EAC test certificates, packing lists, invoices and full customs documentation are included with every shipment.</div>
    </div>
    <div class="faq-item">
      <div class="q" data-i18n="faq.q3">What is the minimum order quantity?</div>
      <div class="a" data-i18n="faq.a3">No fixed minimum for standard configurations — tell us your project needs and we will advise the most economical drum lengths.</div>
    </div>
    <div class="faq-item">
      <div class="q" data-i18n="faq.q4">Can you supply custom conductor sizes and screens?</div>
      <div class="a" data-i18n="faq.a4">Yes. Our factory supports custom cross-sections, copper screens and armour options; send your specification for a free technical proposal.</div>
    </div>
    <div class="faq-item">
      <div class="q" data-i18n="faq.q5">How do I get a fast price indication?</div>
      <div class="a" data-i18n="faq.a5">Email or WhatsApp your voltage, conductor, length and quantity — you will receive an indicative price within one business day.</div>
    </div>
  </div>
</section>
'''

# ---- assemble I18N js ----
def jsval(s):
    return json.dumps(s, ensure_ascii=False)

i18n_parts = []
for lang in ['en', 'ru', 'es', 'ar', 'zh', 'fr', 'uk', 'tr', 'de', 'pt', 'mn']:
    d = T[lang]
    pairs = [f'"{k}":{jsval(v)}' for k, v in d.items()]
    i18n_parts.append(f'{lang}:{{\n' + ',\n'.join(pairs) + '\n}')
i18n_js = 'var I18N={\n' + ',\n'.join(i18n_parts) + '\n};\n'

# ---- build script (applyLang part reused from source) ----
apply_src = applyjs
# replace I18N block only
new_script = '<script>\n' + i18n_js + apply_src[apply_src.find('function setLang'):]

# ---- JSON-LD ----
ld = '''<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Article","headline":"35 kV Computing Power Cable for AI Data Centers — OUZHI Cable Source Factory","url":"https://ouzcable.com/ai-computing.html","author":{"@type":"Organization","name":"OUZHI Cable","alternateName":"欧智电缆"},"publisher":{"@type":"Organization","name":"OUZHI Cable","logo":"https://ouzcable.com/logo-en.png"},"description":"35 kV computing power cables for AI data centers and computing hubs: XLPE insulation, copper conductor, LSZH fire-safe sheath, IEC/GOST certified, factory-direct from OUZHI Cable source factory. Contact info@ouzcable.com | +998 99 851 6999.","mainEntity":{"@type":"Organization","name":"OUZHI Cable","email":"info@ouzcable.com","telephone":"+998998516999"}}
</script>'''

# ---- head ----
head = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>35 kV Computing Power Cable for AI Data Centers | Source Factory — OUZHI Cable 欧智电缆 | 35KV算力电缆源头工厂</title>
<meta name="description" content="35 kV computing power cable (算力电缆) for AI data centers and computing hubs: 26/35 kV XLPE, copper conductor, copper screen, LSZH fire-safe sheath. IEC 60502-2 & GOST 31996 certified, 100% factory-tested, factory-direct from OUZHI Cable source factory. Export to Central Asia, Middle East, Russia, Europe, Americas, Uzbekistan, Kazakhstan, Turkey, Germany, Malaysia, Mexico. Contact: info@ouzcable.com | +998 99 851 6999.">
<meta name="keywords" content="35kV computing power cable, 35KV算力电缆, AI data center power cable, data center cable supplier, computing hub cable, AI GPU cluster cable, 35kV cable for data centers, LSZH medium voltage cable, IEC 60502-2 35kV cable, GOST 31996 cable, source factory cable manufacturer, cable factory China, OUZHI Cable, 欧智电缆, medium voltage cable export, Uzbekistan cable supplier, Kazakhstan cable, Turkey cable import, Germany MV cable, Malaysia cable, Mexico cable">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="author" content="OUZHI Cable">
<link rel="canonical" href="https://ouzcable.com/ai-computing.html">
<link rel="alternate" hreflang="en" href="https://ouzcable.com/ai-computing.html?lang=en">
<link rel="alternate" hreflang="zh" href="https://ouzcable.com/ai-computing.html?lang=zh">
<link rel="alternate" hreflang="ru" href="https://ouzcable.com/ai-computing.html?lang=ru">
<link rel="alternate" hreflang="ar" href="https://ouzcable.com/ai-computing.html?lang=ar">
<link rel="alternate" hreflang="fr" href="https://ouzcable.com/ai-computing.html?lang=fr">
<link rel="alternate" hreflang="de" href="https://ouzcable.com/ai-computing.html?lang=de">
<link rel="alternate" hreflang="uk" href="https://ouzcable.com/ai-computing.html?lang=uk">
<link rel="alternate" hreflang="es" href="https://ouzcable.com/ai-computing.html?lang=es">
<link rel="alternate" hreflang="tr" href="https://ouzcable.com/ai-computing.html?lang=tr">
<link rel="alternate" hreflang="pt" href="https://ouzcable.com/ai-computing.html?lang=pt">
<link rel="alternate" hreflang="mn" href="https://ouzcable.com/ai-computing.html?lang=mn">
<link rel="alternate" hreflang="x-default" href="https://ouzcable.com/ai-computing.html">
<link rel="icon" type="image/png" href="favicon.png">
'''
head += style
head += '</head>\n<body>\n'

page = head + topbar + '\n' + body + contact_section + '\n' + footer + '\n' + new_script + '\n' + ld + '\n</body>\n</html>\n'

open(OUT, 'w', encoding='utf-8').write(page)
print('written', OUT, len(page), 'bytes')
