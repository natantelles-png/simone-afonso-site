"""Paginas fixas de servicos, neuroarquitetura e sobre (SEO e busca por IA).

Chamado por build_blog.py. Cada pagina e HTML puro, com resposta rapida, FAQ visivel,
JSON-LD (Service, FAQPage, BreadcrumbList, Person, ProfessionalService) e links internos.
Para mudar um texto, edite os dicionarios abaixo e publique.
"""
import json, os, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# chave -> (arquivo no repositorio, texto alternativo)
IMG = {
    'res-sala-varanda': ('assets/servicos/res-sala-varanda.jpg', 'Sala de estar integrada à varanda, com painel de madeira ondulada na parede, sofá cinza-claro, cortinas e luz natural ao fundo'),
    'res-sala-tv': ('assets/servicos/res-sala-tv.jpg', 'Sala de estar com rack de madeira ripada, painel branco com relevo 3D, TV, sofá bege e cortina cinza'),
    'res-painel-tv': ('assets/servicos/res-painel-tv.jpg', 'Painel de TV com iluminação embutida, parede com relevo geométrico, rack de madeira ripada e poltrona ao lado'),
    'res-jantar': ('assets/out3/p_jantar2.jpg', 'Sala de jantar com mesa redonda clara, cadeiras estofadas e lustre de anéis'),
    'res-cozinha': ('assets/out/p_coz1.jpg', 'Cozinha com ilha clara e sanca de luz'),
    'res-quarto': ('assets/out/p_kit1.jpg', 'Quarto de uma kitnete com cabeceira de madeira e roupa de cama clara'),
    'vdb-interior': ('assets/servicos/vdb-loja-interior.jpg', 'Interior amplo da loja Vila do Bem, com jardim vertical, mezanino em madeira e gôndolas de produtos a granel'),
    'vdb-mezanino': ('assets/servicos/vdb-loja-mezanino.jpg', 'Salão da loja Vila do Bem com pé-direito alto, jardim vertical e iluminação natural'),
    'vdb-corredor': ('assets/servicos/vdb-loja-corredor.jpg', 'Corredor da loja Vila do Bem com forro de madeira e gôndolas dos dois lados'),
    'vdb-prateleiras': ('assets/servicos/vdb-loja-prateleiras.jpg', 'Prateleiras de madeira da loja Vila do Bem sob vigas aparentes e luz natural'),
    'vdb-convivencia': ('assets/servicos/vdb-convivencia.jpg', 'Área de convivência da Vila do Bem com banco de madeira, grama e parede com a marca'),
    'vdb-kids': ('assets/servicos/vdb-kids.jpg', 'Espaço Kids da Vila do Bem, com piso lúdico e cores suaves'),
    'bicho': ('assets/out/p_bicho1.jpg', 'Salão comprido do restaurante Bicho Guloso Prime, com teto de madeira, mesas escuras e estofados coloridos'),
    'stand': ('assets/out5/p_stand.jpg', 'Imagem 3D de stand de feira da Vila do Bem, com estrutura de madeira, plantas penduradas e gôndolas'),
    'maelle': ('assets/out/s_estante.jpg', 'Simone Afonso ao lado de uma estante com produtos e uma parede de plantas no Studio Maelle'),
    'bmq-patio': ('assets/servicos/bmq-patio.jpg', 'Pátio externo do Espaço Bem Me Quer, com canteiros de ervas em tijolinhos, piso de madeira e porta de vidro'),
    'bmq-horta': ('assets/servicos/bmq-horta.jpg', 'Horta em canteiros de concreto vista pela porta de vidro do Espaço Bem Me Quer'),
    'bmq-sala': ('assets/servicos/bmq-sala.jpg', 'Sala ampla do Espaço Bem Me Quer com piso de madeira, parede de pedra e porta de vidro para o jardim'),
    'bmq-recepcao': ('assets/servicos/bmq-recepcao.jpg', 'Recepção do Espaço Bem Me Quer com parede amarela, silhueta de meditação e piso de madeira'),
    'bmq-espera': ('assets/servicos/bmq-espera.jpg', 'Sala de espera do Espaço Bem Me Quer com poltronas, parede amarela com frase e pegadas coloridas'),
    'bmq-meditacao': ('assets/servicos/bmq-meditacao.jpg', 'Sala de meditação com parede de pedra, arandelas e uma pequena fonte'),
    'bmq-fisio': ('assets/servicos/bmq-fisio.jpg', 'Sala de fisioterapia do Espaço Bem Me Quer com barras paralelas e maca azul'),
    'switch': ('assets/v2/43938a1e41c2a37861cdbe8c7a205c7e.webp', 'Imagem 3D do escritório da Switch, com bancadas de trabalho, parede roxa com ondas, jardim vertical e sala envidraçada ao fundo'),
    'rl-sala-antes': ('assets/out/ad_sala_antes.jpg', 'Antes: sala de jantar com mesa de vidro e cadeiras de fibra diante de cortinas verticais'),
    'rl-sala-depois': ('assets/out/ad_sala_depois.jpg', 'Depois: a mesma sala com mesa redonda clara, cadeiras estofadas, lustre de anéis e planta'),
    'rl-menina-antes': ('assets/out/ad_menina_antes.jpg', 'Antes: escrivaninha de quarto infantil com fios aparentes, medalhas e objetos acumulados'),
    'rl-menina-depois': ('assets/out/ad_menina_depois.jpg', 'Depois: quarto infantil com cama azul, prateleiras, painel iluminado e adesivo de cavalo na parede'),
    'rl-cozinha-antes': ('assets/out/ad_cozinha_antes.jpg', 'Antes: cozinha com armários brancos, geladeira e cadeiras de plástico'),
    'rl-cozinha-depois': ('assets/out/ad_cozinha_depois.jpg', 'Depois: cozinha integrada com portas verdes, mesa clara e cadeiras escuras'),
    'rl-compacta-antes': ('assets/out/ad_compacta_antes.jpg', 'Antes: cozinha compacta com fogão e bancada preta'),
    'rl-compacta-depois': ('assets/out/ad_compacta_depois.jpg', 'Depois: cozinha compacta com revestimento geométrico azul e bancada renovada'),
    'hs-1': ('assets/servicos/staging-parabiago-1.jpg', 'Casa de Parabiago depois do Home Staging, com fachada pintada, paisagismo iluminado e muro com gradil, ao entardecer'),
    'hs-2': ('assets/servicos/staging-parabiago-2.jpg', 'Casa de Parabiago depois do Home Staging, vista de outro ângulo ao entardecer'),
    'hs-3': ('assets/servicos/staging-parabiago-3.jpg', 'Casa de Parabiago depois do Home Staging, com árvore e jardim iluminados'),
    'hs-4': ('assets/servicos/staging-parabiago-4.jpg', 'Casa de Parabiago depois do Home Staging, fachada em tom verde ao entardecer'),
    'neuro-bebe': ('assets/out/p_bebe.jpg', 'Quarto de bebê com nuvem verde iluminada, cortina branca e prateleira com bichos de pelúcia'),
    'simone': ('assets/v2/50f522c81d55920289521c1bfa69f256.webp', 'Simone Afonso, arquiteta, de blazer listrado, sorrindo'),
    'consultoria': ('assets/out/s_verde.jpg', 'Simone Afonso ao lado de uma parede de plantas, avaliando o ambiente'),
}

AREAS = 'Vitória, Vila Velha, Serra, Cariacica, Guarapari e todo o Espírito Santo, na sua casa ou empresa e também online'
COMO = [
    ('Conversa e briefing', 'Entendo quem usa o espaço, a rotina, o que incomoda e o que você quer sentir ali. A conversa é online ou na sua casa ou empresa.'),
    ('Visita técnica', 'Meço e analiso o espaço: luz, ventilação, ruído, circulação e o que pode ser aproveitado.'),
    ('Proposta e projeto', 'Você vê o layout e as vistas em 3D antes de aprovar, para decidir com segurança.'),
    ('Obra e entrega', 'Coordeno os profissionais que executam e confiro cada detalhe até o espaço ficar pronto.'),
]

S = [
    {
        'slug': 'projetos-residenciais', 'nome': 'Projetos residenciais',
        'title': 'Projeto de arquitetura de interiores residencial em Vitória (ES) | Simone Afonso',
        'desc': 'Projeto completo de interiores para casas e apartamentos em Vitória e no Espírito Santo, do briefing à obra, com 3D, documentação técnica e coordenação da execução.',
        'h1': 'Projeto de interiores residencial em Vitória (ES)',
        'resposta': 'O projeto residencial da Simone Afonso cobre briefing, layout, vistas em 3D, documentação técnica e coordenação da obra. Serve para quem vai reformar uma casa ou apartamento no Espírito Santo e quer decidir com segurança, vendo tudo antes de aprovar. O valor é definido após a visita técnica.',
        'intro': [
            'Um projeto residencial começa na vida de quem mora na casa, não em um catálogo. Eu converso sobre a rotina, as manias, os móveis que ficam e o que você quer sentir em cada ambiente, e transformo isso em um projeto de interiores completo.',
            'A Neuroarquitetura orienta o olhar: luz natural, conforto acústico, cores, circulação e organização influenciam o humor e o descanso de quem vive no espaço. O resultado é uma casa funcional e com a sua cara.',
        ],
        'para': 'Quem vai reformar ou montar a casa ou o apartamento e quer decidir com segurança, vendo tudo antes de aprovar.',
        'inclui': ['Briefing funcional e emocional', 'Planta com o novo layout', 'Vistas em 3D para aprovar antes da obra', 'Projeto de iluminação, marcenaria e especificação de materiais', 'Documentação técnica para os profissionais que executam', 'Coordenação e acompanhamento da obra'],
        'fotos': ['res-sala-varanda', 'res-jantar', 'res-sala-tv', 'res-painel-tv', 'res-cozinha', 'res-quarto'],
        'depo': ('Nosso apartamento ficou a “nossa cara” e é um prazer morar e receber pessoas queridas em nosso “novo” espaço.', 'Andrea Mongin, reforma completa de apartamento'),
        'faq': [
            ('Quanto custa um projeto de interiores residencial?', 'O valor varia porque depende da complexidade e do tamanho do espaço. Ele é definido depois da visita técnica, quando eu entendo o espaço e o que você precisa. Aceito cartão de crédito, depósito bancário e Pix.'),
            ('O projeto inclui o acompanhamento da obra?', 'Sim. Eu coordeno os profissionais que executam e tenho parceiros de confiança em todas as áreas da obra.'),
            ('Eu vejo o resultado antes de a obra começar?', 'Sim. Você aprova a planta e as vistas em 3D antes da execução, o que evita surpresas e retrabalho.'),
            ('Você atende apartamentos pequenos?', 'Sim. Espaços compactos pedem ainda mais atenção a circulação, armazenamento e luz, e costumam render projetos muito funcionais.'),
            ('Vale mais a pena um projeto completo ou o Home Relooking?', 'Se o espaço precisa mudar a planta ou trocar acabamentos, o caminho é o projeto completo. Se basta renovar com mudanças pontuais, o Home Relooking custa menos. Eu indico o melhor na visita.'),
        ],
        'rel': ['home-relooking', 'consultoria', 'neuroarquitetura'],
    },
    {
        'slug': 'projetos-comerciais', 'nome': 'Projetos comerciais',
        'title': 'Projeto comercial: arquitetura para lojas e restaurantes em Vitória (ES) | Simone Afonso',
        'desc': 'Arquitetura comercial para lojas, restaurantes, consultórios e empresas no Espírito Santo, com Neuroarquitetura, layout, identidade da marca e acompanhamento da obra.',
        'h1': 'Projeto comercial para lojas e restaurantes em Vitória (ES)',
        'resposta': 'Projetos comerciais da Simone Afonso traduzem a identidade e o propósito de um negócio em um espaço que acolhe clientes e equipe. Ela atende lojas, restaurantes, consultórios, escritórios e empresas no Espírito Santo, com layout, iluminação, materiais e coordenação da obra, orientados pela Neuroarquitetura.',
        'intro': [
            'Cada negócio tem uma identidade, um propósito e pessoas que dão sentido a ele. Meu trabalho é compreender essa relação e traduzi-la em espaços que acolham, facilitem a rotina e favoreçam a experiência de quem compra, é atendido ou trabalha ali.',
            'Projetos comerciais são os que eu mais gosto de fazer. A loja Vila do Bem, o restaurante Bicho Guloso Prime e o Studio Maelle estão entre os trabalhos. Também aplico a minha especialização em Ambientes de Trabalho, com certificação alemã.',
        ],
        'para': 'Lojas, restaurantes, consultórios, escritórios e empresas que desejam expressar a marca no espaço e cuidar da experiência de clientes e equipes.',
        'inclui': ['Layout e circulação pensados para as pessoas e a rotina do negócio', 'Identidade e propósito da marca traduzidos no ambiente', 'Iluminação, materiais, cores e conforto sensorial', 'Organização dos espaços para apoiar o trabalho e o bem-estar da equipe', 'Vistas em 3D para aprovar antes da obra', 'Coordenação e acompanhamento da obra'],
        'fotos': ['vdb-interior', 'vdb-mezanino', 'vdb-prateleiras', 'vdb-corredor', 'bicho', 'stand', 'maelle'],
        'cases': 'Vila do Bem (Praia do Canto e Praia da Costa), Bicho Guloso Prime, Studio Maelle, stand da Vila do Bem em feira e clínica veterinária Toca dos Animais.',
        'depo': ('Não é apenas sobre onde fica cada móvel, mas sobre como transformar uma sala comercial em um ambiente em que as nossas clientes se sintam em casa.', 'Cassia Bastianelle, sócia do Estúdio Maelle'),
        'faq': [
            ('Você faz projetos comerciais e corporativos?', 'Sim, e são os que eu mais gosto de fazer. Atendo lojas, restaurantes, escritórios, empresas e indústrias. Tenho especialização em Ambientes de Trabalho com certificação alemã.'),
            ('O que a Neuroarquitetura muda em uma loja?', 'Ela orienta decisões como iluminação, cores, ruído, circulação e organização, que influenciam como as pessoas se sentem e se comportam no espaço. O objetivo é uma experiência mais acolhedora para clientes e equipe.'),
            ('Quanto custa um projeto comercial?', 'Depende da complexidade e do tamanho do espaço. O valor é definido depois da visita técnica.'),
            ('Você acompanha a obra da loja?', 'Sim. Eu coordeno os profissionais que executam e acompanho até a entrega, para que o resultado seja o que foi projetado.'),
            ('Atende fora da Grande Vitória?', 'Atendo todo o Espírito Santo, com foco na Grande Vitória, e também online. Já fiz projetos em São Paulo e Minas Gerais.'),
        ],
        'rel': ['projetos-corporativos', 'projetos-institucionais', 'neuroarquitetura'],
    },
    {
        'slug': 'projetos-institucionais', 'nome': 'Projetos institucionais',
        'title': 'Projeto institucional: espaços de acolhimento e cuidado no ES | Simone Afonso',
        'desc': 'Projetos de arquitetura para associações, ONGs e clínicas: acessibilidade, cores, luz e áreas verdes pensadas para acolher. Caso: Espaço Bem Me Quer, da ACACCI.',
        'h1': 'Projeto institucional para associações, ONGs e clínicas no Espírito Santo',
        'resposta': 'Projetos institucionais da Simone Afonso criam espaços de acolhimento para associações, ONGs e clínicas, com acessibilidade, cores, luz natural e áreas verdes orientadas pela Neuroarquitetura. O Espaço Bem Me Quer, da ACACCI, é um exemplo: um espaço com recepção, salas de atendimento, jardim e horta.',
        'intro': [
            'Instituições que cuidam de pessoas precisam de espaços que acalmem e recebam bem. No Espaço Bem Me Quer, da ACACCI, o projeto reuniu recepção, salas de atendimento, fisioterapia, sala de meditação e um pátio com horta, tudo pensado para quem cuida e para quem é cuidado.',
            'Nesses projetos o orçamento costuma ser enxuto e a identidade da instituição importa muito. Cores, frases e áreas verdes entram como parte do cuidado, sem perder a acessibilidade e a praticidade do dia a dia.',
        ],
        'para': 'Associações, ONGs, clínicas e instituições que querem um espaço acolhedor, acessível e com a identidade do seu propósito.',
        'inclui': ['Acessibilidade e circulação para todas as pessoas', 'Cores e frases que acolhem, com a identidade da instituição', 'Áreas externas, jardins e horta como parte do cuidado', 'Salas de atendimento, espera e convivência', 'Orçamento enxuto e coordenação da obra'],
        'fotos': ['bmq-patio', 'bmq-horta', 'bmq-sala', 'bmq-recepcao', 'bmq-espera', 'bmq-meditacao', 'bmq-fisio'],
        'cases': 'Espaço Bem Me Quer, da ACACCI.',
        'depo': None,
        'faq': [
            ('O que é o Espaço Bem Me Quer?', 'É um espaço de acolhimento da ACACCI, projetado pela Simone Afonso, com recepção, salas de atendimento, fisioterapia, sala de meditação e um pátio com horta.'),
            ('Você atende ONGs e associações com orçamento limitado?', 'Sim. Os projetos institucionais pedem soluções enxutas, com prioridade para acessibilidade, conforto e acolhimento. O valor é definido depois da visita técnica.'),
            ('Como a Neuroarquitetura entra em um espaço de cuidado?', 'Pela escolha de luz natural, cores, ruído, circulação e áreas verdes, que ajudam a acalmar e a receber bem quem chega.'),
            ('Você cuida da acessibilidade?', 'Sim. Rampas, circulação livre, banheiros acessíveis e barras de apoio entram no projeto desde o início.'),
        ],
        'rel': ['projetos-comerciais', 'projetos-corporativos', 'neuroarquitetura'],
    },
    {
        'slug': 'projetos-corporativos', 'nome': 'Projetos corporativos',
        'title': 'Projeto corporativo: escritórios e ambientes de trabalho no ES | Simone Afonso',
        'desc': 'Arquitetura corporativa para indústrias e empresas no Espírito Santo: ambientes de trabalho saudáveis, seguros e com a identidade da empresa, com certificação alemã em Ambientes de Trabalho.',
        'h1': 'Projeto corporativo: escritórios, indústrias e ambientes de trabalho',
        'resposta': 'Projetos corporativos da Simone Afonso criam ambientes de trabalho para indústrias e empresas pensados para a saúde, a segurança e o bem-estar das equipes. Ela aplica a especialização em Ambientes de Trabalho, com certificação alemã, junto com a Neuroarquitetura, em escritórios e áreas operacionais no Espírito Santo.',
        'intro': [
            'Pessoas passam boa parte do dia no trabalho, e o ambiente pesa no foco, no cansaço e na convivência. Um projeto corporativo bem pensado organiza fluxos, cuida da ergonomia e cria áreas de descanso e convivência.',
            'Apliquei esse olhar em escritórios como o da Switch e em projetos para indústrias. A identidade da empresa aparece no espaço sem prejudicar a segurança e a operação.',
        ],
        'para': 'Indústrias e empresas que querem ambientes de trabalho mais funcionais, saudáveis e com a cara da empresa.',
        'inclui': ['Layout e fluxos pensados para a rotina e a segurança da operação', 'Ergonomia, iluminação e conforto térmico e acústico', 'Áreas de convivência e descanso para as equipes', 'Identidade da empresa traduzida no ambiente', 'Vistas em 3D e coordenação da obra'],
        'fotos': ['switch'],
        'cases': 'Escritório da Switch e projetos para indústrias.',
        'depo': None,
        'faq': [
            ('O que é a especialização em Ambientes de Trabalho com certificação alemã?', 'É a formação da Simone voltada a ambientes de trabalho saudáveis e seguros, que ela aplica em escritórios e áreas operacionais junto com a Neuroarquitetura.'),
            ('Você projeta para indústrias?', 'Sim. Projetos para indústrias e empresas estão entre os atendimentos, com atenção a fluxos, segurança, ergonomia e áreas de descanso.'),
            ('Posso ver o escritório em 3D antes da obra?', 'Sim. Você aprova o layout e as vistas em 3D antes de qualquer execução.'),
            ('Quanto custa?', 'O valor depende da complexidade e do tamanho do espaço e é definido depois da visita técnica.'),
        ],
        'rel': ['projetos-comerciais', 'consultoria', 'neuroarquitetura'],
    },
    {
        'slug': 'home-relooking', 'nome': 'Home Relooking',
        'title': 'Home Relooking: renovar a casa sem reforma em Vitória (ES) | Simone Afonso',
        'desc': 'Home Relooking é a renovação da casa por mudanças pontuais, como arrumação dos móveis, iluminação, pintura e tecidos. Custa menos que uma reforma completa. Veja antes e depois.',
        'h1': 'Home Relooking: renovar a casa sem fazer uma reforma',
        'resposta': 'Home Relooking é a renovação de um ambiente por mudanças pontuais, como nova arrumação dos móveis, ajuste da iluminação, pintura, troca de tecidos e peças novas, aproveitando o que já existe. Custa menos que uma reforma completa. A Simone Afonso indica na visita se o seu caso pede Relooking ou um projeto completo.',
        'intro': [
            'Nem toda casa precisa de uma reforma. Muitas vezes o espaço já tem boas peças e só precisa de um novo olhar para ficar confortável e com a sua cara.',
            'No Home Relooking eu valorizo o que já existe e considero a rotina e a história de quem mora ali. A mudança vem da arrumação, da luz, das cores e de poucas peças certas.',
        ],
        'para': 'Quem quer uma casa mais confortável e com a sua cara, sem mudar tudo.',
        'inclui': ['Nova arrumação dos móveis', 'Ajuste da iluminação', 'Pintura e troca de tecidos', 'Peças novas onde fazem diferença'],
        'fotos': ['rl-sala-antes', 'rl-sala-depois', 'rl-menina-antes', 'rl-menina-depois', 'rl-cozinha-antes', 'rl-cozinha-depois', 'rl-compacta-antes', 'rl-compacta-depois'],
        'depo': None,
        'faq': [
            ('Home Relooking ou reforma: qual eu preciso?', 'O Home Relooking resolve com mudanças pontuais, como arrumação dos móveis, iluminação, pintura e tecidos. Se o espaço precisa mudar a planta ou trocar acabamentos, o caminho é o projeto completo. Eu indico o melhor na visita.'),
            ('Home Relooking é mais barato que uma reforma?', 'Sim, costuma custar menos que uma reforma completa, porque aproveita o que já existe. O valor exato é definido depois da visita.'),
            ('Preciso comprar móveis novos?', 'Não necessariamente. Só indico peças novas onde elas fazem diferença.'),
            ('Em quanto tempo o espaço muda?', 'Como não há quebra-quebra, o espaço muda mais rápido que em uma reforma. O prazo depende do que for combinado na proposta.'),
        ],
        'rel': ['projetos-residenciais', 'home-staging', 'consultoria'],
    },
    {
        'slug': 'home-staging', 'nome': 'Home Staging',
        'title': 'Home Staging: preparar o imóvel para vender ou alugar no ES | Simone Afonso',
        'desc': 'Home Staging é a preparação do imóvel para vender ou alugar: arrumação dos móveis, iluminação, pintura, pequenos reparos e objetos para fotos e visitas, com consultoria e relatório.',
        'h1': 'Home Staging: preparar o imóvel para vender ou alugar',
        'resposta': 'Home Staging é a preparação de um imóvel para vender ou alugar, com consultoria e relatório que organizam e valorizam o espaço: arrumação dos móveis, iluminação, pintura, pequenos reparos e objetos para as fotos e as visitas. O objetivo é que quem visita perceba as qualidades do imóvel e se imagine vivendo ali.',
        'intro': [
            'A primeira impressão decide muito na hora de vender ou alugar. Um imóvel organizado, bem iluminado e com ambientes que fazem sentido é visto com mais clareza por quem visita.',
            'Na consultoria de Home Staging eu avalio o imóvel, entrego um relatório com o que ajustar e posso acompanhar a preparação para as fotos e as visitas. Na casa de Parabiago, as mudanças de pintura e paisagismo renovaram a fachada.',
        ],
        'para': 'Quem vai vender ou alugar e quer causar uma boa primeira impressão.',
        'inclui': ['Arrumação dos móveis', 'Iluminação', 'Pintura e pequenos reparos', 'Objetos para as fotos e as visitas', 'Relatório com o que ajustar'],
        'fotos': ['hs-1', 'hs-2', 'hs-3', 'hs-4'],
        'depo': None,
        'faq': [
            ('O que é Home Staging?', 'É a preparação de um imóvel para venda ou aluguel, com ajustes de arrumação, luz, pintura e objetos que valorizam o espaço nas fotos e nas visitas.'),
            ('Home Staging serve para alugar também?', 'Sim. Qualquer imóvel que precise causar boa primeira impressão pode se beneficiar, seja para venda ou aluguel.'),
            ('Preciso fazer reforma antes?', 'Em geral não. O Home Staging trabalha com pintura, pequenos reparos e organização, sem obra pesada.'),
            ('Quanto custa?', 'O valor é definido depois da visita técnica, de acordo com o tamanho do imóvel e o que for combinado.'),
        ],
        'rel': ['home-relooking', 'projetos-residenciais', 'consultoria'],
    },
    {
        'slug': 'consultoria', 'nome': 'Consultoria',
        'title': 'Consultoria de arquitetura e interiores por hora no ES | Simone Afonso',
        'desc': 'Consultoria por horas, na sua casa ou empresa, para orientar decisões de layout, cores e materiais, com relatório e especificações, sem precisar de um projeto completo.',
        'h1': 'Consultoria de arquitetura e interiores',
        'resposta': 'A consultoria da Simone Afonso é um serviço por horas, na sua casa ou empresa, para orientar decisões de layout, cores e materiais. Inclui visita técnica e relatório com especificações, sem a necessidade de um projeto completo. Serve para quem já tem uma ideia e precisa de um olhar técnico para acertar.',
        'intro': [
            'Nem sempre é preciso um projeto completo. Às vezes você já sabe o que quer e só precisa de alguém que olhe o espaço com olhar técnico e aponte o melhor caminho.',
            'Na consultoria eu visito o espaço, oriento sobre layout, cores e materiais e entrego um relatório com as especificações, para você executar com segurança.',
        ],
        'para': 'Quem já tem uma ideia e precisa de um olhar técnico para acertar.',
        'inclui': ['Visita técnica', 'Orientação sobre layout, cores e materiais', 'Relatório com especificações'],
        'fotos': ['consultoria', 'maelle'],
        'depo': ('A consultoria com a Simone foi essencial para mapear cada cantinho do Stúdio, tornar os ambientes funcionais e ainda trazer aconchego e acolhimento.', 'Cassia Bastianelle, Estúdio Maelle'),
        'faq': [
            ('Como funciona a consultoria?', 'São horas de orientação no seu espaço, com visita técnica, recomendações de layout, cores e materiais e um relatório com especificações.'),
            ('Qual a diferença entre consultoria e projeto?', 'A consultoria orienta as decisões e entrega um relatório. O projeto completo inclui planta, vistas em 3D, documentação técnica e coordenação da obra.'),
            ('Atende empresas?', 'Sim. A consultoria vale para casas, lojas, escritórios e outros espaços.'),
            ('Quanto custa?', 'O valor depende das horas e do tipo de espaço e é combinado antes.'),
        ],
        'rel': ['projetos-residenciais', 'projetos-comerciais', 'home-staging'],
    },
]
BYSLUG = {s['slug']: s for s in S}


def build(B):
    """B e o modulo build_blog (head, foot, entities, jsonld, write, wa, SITE, CFG, esc, OUT...)."""
    SITE, CFG, esc, wa = B.SITE, B.CFG, B.esc, B.wa
    out_img = os.path.join(B.OUT, 'servicos', 'img')
    os.makedirs(out_img, exist_ok=True)
    dims = {}
    for k, (path, _alt) in IMG.items():
        src = os.path.join(ROOT, path)
        if not os.path.exists(src):
            print('  aviso: imagem de servico ausente', path)
            continue
        ext = os.path.splitext(src)[1]
        shutil.copy(src, os.path.join(out_img, k + ext))
        try:
            from PIL import Image
            w, h = Image.open(src).size
        except Exception:
            w = h = None
        dims[k] = (f'/servicos/img/{k}{ext}', w, h)

    def fig(k, eager=False, cls=''):
        if k not in dims:
            return ''
        src, w, h = dims[k]
        d = f' width="{w}" height="{h}"' if w else ''
        ld = ' fetchpriority="high"' if eager else ' loading="lazy"'
        return f'<figure class="foto {cls}"><img src="{src}" alt="{esc(IMG[k][1], True)}"{d}{ld} decoding="async"></figure>'

    person, biz, site = B.entities()
    today_iso = B.dt.datetime.now(B.dt.timezone(B.dt.timedelta(hours=-3))).strftime('%Y-%m-%d')
    pages = []  # (path, lastmod, image)

    def page(path, title, desc, h1, kicker, resposta, body_html, crumbs, faq, extra_graph, og_img=None, tail=''):
        url = SITE + path
        graph = [person, biz, site, {
            '@type': 'WebPage', '@id': url + '#pagina', 'url': url, 'name': title, 'description': desc, 'inLanguage': 'pt-BR',
            'isPartOf': {'@id': SITE + '/#site'}, 'about': {'@id': SITE + '/#negocio'},
            'speakable': {'@type': 'SpeakableSpecification', 'cssSelector': ['h1', '.resposta p']}},
            {'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': SITE + u} for i, (n, u) in enumerate(crumbs)]}]
        graph += extra_graph
        if faq:
            graph.append({'@type': 'FAQPage', '@id': url + '#faq', 'mainEntity': [
                {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faq]})
        h = B.head(title, desc, path, og_img, 'website', B.jsonld({'@context': 'https://schema.org', '@graph': graph}))
        trilha = '<nav class="trilha" aria-label="Você está em"><ol>' + ''.join(
            f'<li><a href="{u}">{esc(n)}</a></li>' for n, u in crumbs[:-1]) + f'<li aria-current="page">{esc(crumbs[-1][0])}</li></ol></nav>'
        faqh = ''
        if faq:
            faqh = '<section class="faq" aria-labelledby="faq-t"><h2 id="faq-t">Perguntas frequentes</h2><dl>' + ''.join(
                f'<dt>{esc(q)}</dt><dd><p>{esc(a)}</p></dd>' for q, a in faq) + '</dl></section>'
        res = f'<aside class="resposta" aria-label="Resposta rápida"><span class="rotulo">Resposta rápida</span><p>{esc(resposta)}</p></aside>' if resposta else ''
        html_ = h + f'''<div class="wrap pagina">
{trilha}
<header class="cab"><span class="kicker">{esc(kicker)}</span><h1>{esc(h1)}</h1></header>
{res}
{body_html}
{faqh}
{tail}
</div>
''' + B.foot()
        B.write(path.lstrip('/') + 'index.html', html_)
        pages.append((path, today_iso, SITE + og_img if og_img else None))

    def cta(msg, titulo='Vamos conversar sobre o seu espaço?'):
        return (f'<section class="cta" aria-labelledby="cta-t"><h2 id="cta-t">{esc(titulo)}</h2>'
                f'<p>Conte para a Simone o que você precisa. A conversa é online ou na sua casa ou empresa, sem compromisso.</p>'
                f'<a class="botao" href="{wa(msg)}">Chamar no WhatsApp</a></section>')

    def rel_links(slugs):
        return '<section class="relacionados-s" aria-labelledby="rel-s"><h2 id="rel-s">Veja também</h2><ul class="lista-links">' + ''.join(
            (f'<li><a href="/servicos/{s}/">{esc(BYSLUG[s]["nome"])}</a></li>' if s in BYSLUG else f'<li><a href="/{s}/">Neuroarquitetura: o que é e como aplicar</a></li>') for s in slugs) + '</ul></section>'

    # ---------------------------------------------------------- paginas de servico
    for s in S:
        path = f'/servicos/{s["slug"]}/'
        url = SITE + path
        svc = {'@type': 'Service', '@id': url + '#servico', 'name': s['nome'], 'serviceType': s['nome'], 'description': s['desc'],
               'url': url, 'provider': {'@id': SITE + '/#negocio'}, 'inLanguage': 'pt-BR',
               'areaServed': [{'@type': 'AdministrativeArea', 'name': 'Espírito Santo'}, {'@type': 'City', 'name': 'Vitória'}, {'@type': 'City', 'name': 'Vila Velha'}, {'@type': 'City', 'name': 'Serra'}],
               'audience': {'@type': 'Audience', 'audienceType': s['para']}}
        fotos = s['fotos']
        ig = ''
        if len(fotos) > 1:
            ig = '<div class="galeria">' + ''.join(fig(k) for k in fotos[1:]) + '</div>'
        cases = f'<p><strong>Trabalhos:</strong> {esc(s["cases"])}</p>' if s.get('cases') else ''
        depo = ''
        if s.get('depo'):
            depo = f'<blockquote class="depo"><p>“{esc(s["depo"][0])}”</p><footer>{esc(s["depo"][1])}</footer></blockquote>'
        passos = '<ol class="passos">' + ''.join(f'<li><strong>{esc(a)}.</strong> {esc(b)}</li>' for a, b in COMO) + '</ol>'
        body = f'''{fig(fotos[0], True, 'capa-s')}
<div class="duas">
<div class="texto">
{''.join(f'<p>{esc(p)}</p>' for p in s['intro'])}
<h2>Para quem é</h2><p>{esc(s['para'])}</p>
<h2>O que está incluído</h2>
<ul class="check">{''.join(f'<li>{esc(i)}</li>' for i in s['inclui'])}</ul>
<h2>Como funciona</h2>{passos}
{cases}
<h2>Onde atendo</h2><p>{esc(AREAS)}.</p>
</div>
<aside class="lateral"><div class="ficha"><h2>Resumo</h2><dl>
<dt>Serviço</dt><dd>{esc(s['nome'])}</dd>
<dt>Profissional</dt><dd>{esc(CFG['author'])}, {esc(CFG['author_role'].lower())}</dd>
<dt>Atendimento</dt><dd>Online e a domicílio</dd>
<dt>Região</dt><dd>Grande Vitória e todo o Espírito Santo</dd>
<dt>Valor</dt><dd>Definido após a visita técnica</dd></dl>
<a class="botao" href="{wa('Olá, Simone! Vim pelo site e gostaria de saber mais sobre ' + s['nome'].lower() + '.')}">Chamar no WhatsApp</a></div></aside>
</div>
{ig}
{depo}
'''
        faq = s['faq']
        body2 = cta('Olá, Simone! Vim pelo site e gostaria de conversar sobre ' + s['nome'].lower() + '.') + rel_links(s['rel'])
        page(path, s['title'], s['desc'], s['h1'], 'Serviço', s['resposta'], body, [('Início', '/'), ('Serviços', '/servicos/'), (s['nome'], path)], faq, [svc],
             og_img=dims[fotos[0]][0] if fotos[0] in dims else None, tail=body2)

    # ---------------------------------------------------------- hub /servicos/
    def thumb(k):
        if k not in dims:
            return ''
        src, w, h = dims[k]
        return f'<img src="{src}" alt="{esc(IMG[k][1], True)}" width="{w}" height="{h}" loading="lazy" decoding="async">'
    cards = ''.join(
        f'<li><article class="card">{thumb(s["fotos"][0])}<div class="info"><h3><a href="/servicos/{s["slug"]}/">{esc(s["nome"])}</a></h3>'
        f'<p>{esc(s["resposta"].split(". ")[0])}.</p></div></article></li>' for s in S)
    hub_faq = [
        ('Quais serviços a Simone Afonso oferece?', 'Projetos residenciais, comerciais, institucionais e corporativos, Home Relooking, Home Staging e consultoria, em Vitória e em todo o Espírito Santo, com atendimento online e a domicílio.'),
        ('Quanto custa um projeto?', 'O valor varia de projeto para projeto, porque depende da complexidade do trabalho. Ele é definido depois da visita técnica. Aceito cartão de crédito, depósito bancário e Pix.'),
        ('Qual serviço escolher?', 'Para reformar de forma completa, o projeto residencial, comercial, institucional ou corporativo. Para renovar com mudanças pontuais, o Home Relooking. Para vender ou alugar, o Home Staging. Para orientação por horas, a consultoria.'),
    ]
    hub_body = f'''<ul class="grade grade-s">{cards}</ul>
<section class="texto"><h2>Todos os serviços seguem o mesmo cuidado</h2>
<p>Em qualquer serviço, o ponto de partida é a pessoa: como ela vive, trabalha e quer se sentir no espaço. A <a href="/neuroarquitetura/">Neuroarquitetura</a> orienta as decisões de luz, cor, ruído e circulação.</p>
<p>Atendo {esc(AREAS)}.</p></section>
'''
    coll = {'@type': 'ItemList', 'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'url': f'{SITE}/servicos/{s["slug"]}/', 'name': s['nome']} for i, s in enumerate(S)]}
    page('/servicos/', 'Serviços de arquitetura de interiores e neuroarquitetura em Vitória (ES) | Simone Afonso',
         'Projetos residenciais, comerciais, institucionais e corporativos, Home Relooking, Home Staging e consultoria em Vitória e em todo o Espírito Santo.',
         'Serviços de arquitetura de interiores e neuroarquitetura', 'Serviços',
         'A Simone Afonso oferece projetos residenciais, comerciais, institucionais e corporativos, Home Relooking, Home Staging e consultoria em Vitória e em todo o Espírito Santo, com atendimento online e a domicílio. O valor de cada projeto é definido depois da visita técnica.',
         hub_body, [('Início', '/'), ('Serviços', '/servicos/')], hub_faq, [coll], og_img=dims['res-sala-varanda'][0] if 'res-sala-varanda' in dims else None,
         tail=cta('Olá, Simone! Vim pelo site e gostaria de conversar sobre um projeto.'))
    # nada de FAQ duplicado no hub: ele ja foi emitido pelo page()

    # ---------------------------------------------------------- neuroarquitetura (guia)
    neuro_faq = [
        ('O que é neuroarquitetura?', 'É o uso do conhecimento sobre como o cérebro e o corpo reagem ao ambiente para orientar decisões de projeto, como luz, cores, ruído, circulação e organização, de modo a favorecer o bem-estar de quem usa o espaço.'),
        ('Neuroarquitetura é a mesma coisa que decoração?', 'Não. A decoração cuida da aparência. A Neuroarquitetura orienta decisões de projeto, como layout, iluminação e conforto acústico, a partir de como as pessoas vivem e se sentem no espaço.'),
        ('Neuroarquitetura substitui tratamento de saúde?', 'Não. Um ambiente bem projetado pode favorecer o descanso, o foco e o acolhimento, mas não substitui acompanhamento de profissionais de saúde.'),
        ('Dá para aplicar neuroarquitetura em casa pequena?', 'Sim. Luz natural, organização, cores calmas, boa ventilação e áreas de descanso funcionam em qualquer tamanho de espaço.'),
        ('Neuroarquitetura serve para lojas e escritórios?', 'Sim. Em lojas, ajuda na experiência de quem compra. Em escritórios, favorece foco, conforto e convivência da equipe.'),
        ('Quem faz projeto de neuroarquitetura em Vitória (ES)?', 'A arquiteta Simone Afonso, em Vitória, atende casas, lojas, clínicas e escritórios no Espírito Santo, com atendimento online e a domicílio.'),
    ]
    neuro_body = f'''{fig('neuro-bebe', True, 'capa-s')}
<div class="texto">
<p>Neuroarquitetura é a área que aproxima a arquitetura do conhecimento sobre o cérebro e o corpo humano. A ideia é simples: o espaço em que você vive e trabalha influencia o seu humor, o seu sono, a sua atenção e o seu nível de estresse, e o projeto pode ser pensado para ajudar nisso.</p>
<p>Não é um estilo nem uma tendência de decoração. É uma forma de decidir layout, luz, cor, som e organização a partir de como as pessoas realmente vivem cada ambiente.</p>
<h2>O que a neuroarquitetura considera em um projeto</h2>
<ul class="check">
<li><strong>Luz.</strong> A luz natural e a iluminação artificial bem escolhidas ajudam o relógio biológico, o foco e o descanso.</li>
<li><strong>Cores e materiais.</strong> Tons, texturas e acabamentos influenciam a sensação de acolhimento ou de agitação.</li>
<li><strong>Som e conforto acústico.</strong> Ruído constante cansa. Materiais e layout podem reduzi-lo.</li>
<li><strong>Circulação e organização.</strong> Caminhos livres e menos desordem visual diminuem a sobrecarga mental.</li>
<li><strong>Natureza.</strong> Plantas, vistas para o verde e materiais naturais trazem sensação de calma.</li>
<li><strong>Controle e privacidade.</strong> Poder ajustar a luz, a abertura e o isolamento dá segurança a quem usa o espaço.</li>
</ul>
<h2>Onde a neuroarquitetura faz diferença</h2>
<p><strong>Em casa:</strong> quartos que favorecem o sono, salas que reúnem a família e cozinhas funcionais. Veja os <a href="/servicos/projetos-residenciais/">projetos residenciais</a>.</p>
<p><strong>Em lojas e restaurantes:</strong> uma experiência mais acolhedora para quem compra e para quem atende. Veja os <a href="/servicos/projetos-comerciais/">projetos comerciais</a>.</p>
<p><strong>Em clínicas e instituições:</strong> espaços que acalmam e recebem bem, como o Espaço Bem Me Quer. Veja os <a href="/servicos/projetos-institucionais/">projetos institucionais</a>.</p>
<p><strong>Em escritórios e indústrias:</strong> ambientes de trabalho com foco, conforto e segurança. Veja os <a href="/servicos/projetos-corporativos/">projetos corporativos</a>.</p>
<h2>Como a Simone Afonso aplica</h2>
<p>A Simone é arquiteta de interiores e neuroarquiteta em Vitória (ES). Ela começa ouvindo quem vai usar o espaço, visita o ambiente, analisa luz, ruído e circulação e traduz o que você quer sentir em um projeto que pode ser visto em 3D antes da obra.</p>
<p>Quer ler mais? Veja os textos do <a href="/blog/">blog</a> ou <a href="/servicos/">conheça os serviços</a>.</p>
</div>'''
    art = {'@type': 'Article', '@id': SITE + '/neuroarquitetura/#artigo', 'headline': 'Neuroarquitetura: o que é e como aplicar em casas, lojas e escritórios',
           'inLanguage': 'pt-BR', 'author': {'@id': SITE + '/#simone'}, 'publisher': {'@id': SITE + '/#negocio'}, 'dateModified': today_iso, 'datePublished': '2026-11-10',
           'about': 'Neuroarquitetura', 'mainEntityOfPage': SITE + '/neuroarquitetura/'}
    page('/neuroarquitetura/', 'Neuroarquitetura: o que é e como aplicar em casas, lojas e escritórios | Simone Afonso',
         'Entenda o que é neuroarquitetura, o que ela considera em um projeto (luz, cor, som, circulação e natureza) e como aplicar em casas, lojas, clínicas e escritórios.',
         'Neuroarquitetura: o que é e como aplicar', 'Guia',
         'Neuroarquitetura é o uso do conhecimento sobre como o cérebro e o corpo reagem ao ambiente para orientar o projeto, com decisões sobre luz, cores, ruído, circulação e organização que favorecem o bem-estar de quem usa o espaço. Não é um estilo de decoração, e sim uma forma de projetar.',
         neuro_body, [('Início', '/'), ('Neuroarquitetura', '/neuroarquitetura/')], neuro_faq, [art],
         og_img=dims['neuro-bebe'][0] if 'neuro-bebe' in dims else None,
         tail=cta('Olá, Simone! Quero entender como a neuroarquitetura pode ajudar no meu espaço.', 'Quer aplicar neuroarquitetura no seu espaço?'))

    # ---------------------------------------------------------- sobre
    sobre_faq = [
        ('Quem é Simone Afonso?', f'{CFG["bio"]}'),
        ('Qual o número do CAU da Simone Afonso?', 'O registro no CAU é A91391-0 ES.'),
        ('Onde a Simone Afonso atende?', f'{AREAS}.'),
        ('Como falar com a Simone?', f'Pelo WhatsApp {CFG["phone"]} ou pelo Instagram @simoneafonso.arq.'),
    ]
    sobre_body = f'''<div class="duas">
<div class="texto">
<p>{esc(CFG['bio'])}</p>
<p>Minha forma de trabalhar parte de uma ideia: eu não tenho um estilo de projeto. Tenho uma maneira de ouvir, compreender e transformar o que você precisa e quer sentir no espaço. Cada projeto nasce dessa troca.</p>
<h2>Formação e áreas de atuação</h2>
<ul class="check"><li>Arquitetura de interiores</li><li>Neuroarquitetura</li><li>Especialização em Ambientes de Trabalho, com certificação alemã</li><li>Home Relooking e Home Staging</li></ul>
<h2>Trabalhos</h2>
<p>Loja Vila do Bem, Espaço Bem Me Quer (ACACCI), restaurante Bicho Guloso Prime, Studio Maelle, escritório da Switch, além de projetos residenciais em Vitória e no Espírito Santo, e também em São Paulo e Minas Gerais.</p>
<h2>Serviços</h2>
<ul class="lista-links">{''.join(f'<li><a href="/servicos/{s["slug"]}/">{esc(s["nome"])}</a></li>' for s in S)}</ul>
</div>
<aside class="lateral">{fig('simone', True)}<div class="ficha"><h2>Contato</h2><dl><dt>Registro</dt><dd>CAU A91391-0 ES</dd><dt>WhatsApp</dt><dd>{esc(CFG['phone'])}</dd><dt>Instagram</dt><dd><a href="{CFG['instagram']}" rel="noopener">@simoneafonso.arq</a></dd><dt>Atendimento</dt><dd>Online e a domicílio</dd></dl></div></aside>
</div>'''
    about = {'@type': 'AboutPage', '@id': SITE + '/sobre/#pagina', 'url': SITE + '/sobre/', 'mainEntity': {'@id': SITE + '/#simone'}}
    page('/sobre/', 'Simone Afonso: arquiteta de interiores e neuroarquiteta em Vitória (ES)',
         'Conheça Simone Afonso, arquiteta de interiores e neuroarquiteta em Vitória (ES), com especialização em Ambientes de Trabalho e atendimento online e a domicílio.',
         'Simone Afonso, arquiteta de interiores e neuroarquiteta em Vitória (ES)', 'Sobre',
         'Simone Afonso é arquiteta de interiores e neuroarquiteta em Vitória (ES), CAU A91391-0 ES. Projeta casas, lojas, clínicas e escritórios a partir de como as pessoas vivem, sentem e trabalham, e coordena a obra. Atende online e a domicílio, na Grande Vitória e em todo o Espírito Santo.',
         sobre_body, [('Início', '/'), ('Sobre', '/sobre/')], sobre_faq, [about], og_img=dims['simone'][0] if 'simone' in dims else None,
         tail=cta('Olá, Simone! Gostaria de conversar sobre um projeto.'))

    return pages, S
