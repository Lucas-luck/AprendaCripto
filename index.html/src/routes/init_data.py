from flask import Blueprint, jsonify
from src.models.admin import Admin
from src.models.content import Article, AffiliateLink, SeoConfig
from src.models.user import db

init_bp = Blueprint('init', __name__)

@init_bp.route('/init-data', methods=['POST'])
def init_default_data():
    try:
        # Create default admin user
        admin = Admin.query.filter_by(username='admin').first()
        if not admin:
            admin = Admin(username='admin', email='admin@aprendacripto.fun')
            admin.set_password('crypto2025')
            db.session.add(admin)

        # Create default affiliate link (Binance)
        binance_link = AffiliateLink.query.filter_by(name='Binance').first()
        if not binance_link:
            binance_link = AffiliateLink(
                name='Binance',
                url='https://www.binance.com/activity/referral-entry/CPA?ref=CPA_0033D70P8U',
                description='Link de afiliado da Binance para ganhar cashback'
            )
            db.session.add(binance_link)

        # Create default articles
        articles_data = [
            {
                'title': 'Mineração de Criptomoedas',
                'subtitle': 'Entenda o processo que mantém as redes blockchain funcionando e como você pode participar',
                'slug': 'mining',
                'read_time': '8 min',
                'icon_name': 'Pickaxe',
                'color_gradient': 'from-blue-500 to-cyan-500',
                'content': '''A mineração de criptomoedas é o processo fundamental que valida e adiciona novas transações a uma blockchain, além de ser o mecanismo pelo qual novas unidades de criptomoedas são introduzidas no mercado. Em essência, os mineradores utilizam poder computacional para resolver problemas matemáticos complexos.

## Como Funciona a Mineração?

O processo envolve a agregação de transações em blocos, resolução de quebra-cabeças criptográficos através da Prova de Trabalho (PoW), validação pela rede e recompensa aos mineradores com novas moedas e taxas de transação.

## Tipos de Mineração

### Mineração com GPU
Utiliza placas de vídeo para processamento paralelo, ideal para altcoins e mineradores domésticos.

### Mineração ASIC
Hardware especializado para criptomoedas específicas, extremamente eficiente mas caro.

### Mineração em Nuvem
Aluguel de poder de processamento remoto, eliminando a necessidade de hardware próprio.

### Pool de Mineração
Grupos de mineradores que combinam recursos para aumentar chances de recompensa.'''
            },
            {
                'title': 'DeFi - Finanças Descentralizadas',
                'subtitle': 'Descubra o futuro das finanças sem intermediários e as oportunidades de renda passiva',
                'slug': 'defi',
                'read_time': '7 min',
                'icon_name': 'Coins',
                'color_gradient': 'from-green-500 to-emerald-500',
                'content': '''DeFi, ou Finanças Descentralizadas, é um ecossistema de aplicações financeiras construídas sobre redes blockchain, principalmente a Ethereum. O objetivo é recriar serviços financeiros tradicionais de forma descentralizada, sem intermediários como bancos ou corretoras.

## Principais Aplicações DeFi

### Empréstimos Descentralizados
Plataformas como Aave e Compound permitem empréstimos sem intermediários, com taxas definidas por contratos inteligentes.

### Exchanges Descentralizadas (DEXs)
Uniswap e PancakeSwap facilitam trocas diretas entre usuários, sem necessidade de corretoras centralizadas.

### Yield Farming
Estratégia para gerar renda passiva fornecendo liquidez a protocolos DeFi em troca de recompensas.

## Vantagens da DeFi
- Acessibilidade global 24/7
- Transparência total das transações
- Eliminação de intermediários
- Inovação contínua e programabilidade'''
            },
            {
                'title': 'Contratos Inteligentes',
                'subtitle': 'Como a automação está revolucionando acordos e transações na blockchain',
                'slug': 'smart-contracts',
                'read_time': '6 min',
                'icon_name': 'FileText',
                'color_gradient': 'from-purple-500 to-violet-500',
                'content': '''Contratos inteligentes são programas autoexecutáveis armazenados na blockchain que automatizam a execução de acordos quando condições predefinidas são atendidas. Eles eliminam a necessidade de intermediários e garantem execução transparente e imutável.

## Como Funcionam?

1. **Criação**: Código escrito em Solidity
2. **Deploy**: Implantado na blockchain
3. **Execução**: Ativado por condições
4. **Verificação**: Registrado na blockchain

## Aplicações Práticas

### Finanças (DeFi)
Empréstimos automatizados, exchanges descentralizadas e yield farming.

### Seguros
Pagamentos automáticos baseados em dados verificáveis (ex: cancelamento de voos).

### Supply Chain
Rastreamento de produtos e pagamentos automáticos na entrega.

### NFTs e Gaming
Propriedade única de ativos digitais e transações no mercado secundário.'''
            },
            {
                'title': 'Estratégias de Investimento',
                'subtitle': 'Maximize seus retornos com estratégias comprovadas e gestão inteligente de riscos',
                'slug': 'strategies',
                'read_time': '10 min',
                'icon_name': 'TrendingUp',
                'color_gradient': 'from-orange-500 to-red-500',
                'content': '''O sucesso no investimento em criptomoedas requer estratégias bem definidas e gerenciamento de riscos adequado. Explore as principais abordagens utilizadas por investidores experientes para maximizar retornos.

## Estratégias de Longo Prazo

### HODL (Hold On for Dear Life)
Comprar e manter criptomoedas por longos períodos, independentemente das flutuações de curto prazo.
**Vantagens**: Simplicidade, menor estresse, potencial para grandes retornos

### Dollar-Cost Averaging (DCA)
Investir uma quantia fixa em intervalos regulares, reduzindo o impacto da volatilidade.
**Benefícios**: Reduz risco de timing, promove disciplina, adequado para iniciantes

## Estratégias de Trading

### Day Trading
Compra e venda no mesmo dia, aproveitando flutuações de curto prazo.

### Swing Trading
Posições mantidas por dias/semanas, aproveitando tendências médias.

### Scalping
Múltiplas operações rápidas para lucrar com pequenas variações.

## Geração de Renda Passiva

### Staking
Bloquear criptomoedas para apoiar redes PoS e receber recompensas regulares.

### Yield Farming
Fornecer liquidez a protocolos DeFi em troca de tokens de recompensa.

### Crypto Lending
Emprestar criptomoedas para outros usuários e receber juros.

## ⚠️ Gerenciamento de Riscos
- Diversifique seu portfólio entre diferentes criptomoedas
- Nunca invista mais do que pode perder
- Use stop loss e take profit
- Mantenha reservas de emergência
- Faça sua própria pesquisa (DYOR)'''
            },
            {
                'title': 'Guia Completo da Binance',
                'subtitle': 'Tudo que você precisa saber sobre a maior exchange de criptomoedas do mundo',
                'slug': 'binance',
                'read_time': '12 min',
                'icon_name': 'TrendingUp',
                'color_gradient': 'from-yellow-500 to-orange-500',
                'content': '''A Binance é a maior exchange de criptomoedas do mundo por volume de negociação, atendendo mais de 270 milhões de usuários em mais de 180 países. Oferece uma ampla gama de serviços que vão muito além da simples compra e venda de ativos digitais.

## Principais Funcionalidades

### Trading Spot
Compra e venda imediata de mais de 500 criptomoedas com interfaces básica e avançada.
- Ordens market, limit, stop-limit
- Gráficos avançados e indicadores
- Taxas competitivas (0,1% padrão)

### Binance Futures
Trading de futuros com alavancagem de até 125x para amplificar posições.
- Futuros perpétuos e com vencimento
- Margem cross e isolada
- Ferramentas de hedging

### Binance Earn
Produtos para gerar renda passiva com suas criptomoedas.
- Flexible e Locked Savings
- Staking de diversas moedas
- DeFi Staking integrado

### Binance P2P
Negociação direta entre usuários com moedas fiduciárias.
- Mais de 300 métodos de pagamento
- PIX, transferência, cartões
- Sistema de reputação

## Como Começar na Binance

1. **Registro**: Crie sua conta com email
2. **Verificação**: Complete o KYC
3. **Depósito**: Adicione fundos via PIX
4. **Trading**: Comece a investir

## 💡 Dicas de Segurança
- Sempre ative a autenticação de dois fatores (2FA)
- Use senhas fortes e únicas
- Verifique sempre a URL oficial (binance.com)
- Configure whitelist para endereços de saque
- Considere usar carteiras externas para grandes quantias'''
            }
        ]

        for article_data in articles_data:
            existing_article = Article.query.filter_by(slug=article_data['slug']).first()
            if not existing_article:
                article = Article(**article_data)
                db.session.add(article)

        # Create default SEO configs
        seo_configs = [
            {
                'page_slug': 'home',
                'title': 'Aprendacripto - Seu Guia Completo para Investimentos em Criptomoedas',
                'description': 'Aprenda sobre Bitcoin, DeFi, mineração e estratégias de investimento em criptomoedas. Guias completos, análises detalhadas e as melhores oportunidades do mercado cripto.',
                'keywords': 'criptomoedas, bitcoin, ethereum, binance, defi, mineração, investimento, blockchain, trading, yield farming',
                'og_image': '/logo.png'
            }
        ]

        for seo_data in seo_configs:
            existing_seo = SeoConfig.query.filter_by(page_slug=seo_data['page_slug']).first()
            if not existing_seo:
                seo_config = SeoConfig(**seo_data)
                db.session.add(seo_config)

        # Commit all changes
        db.session.commit()

        return jsonify({'message': 'Default data initialized successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

