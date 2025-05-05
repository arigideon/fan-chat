import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv # type: ignore

# Configuração de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Carrega variáveis de ambiente
load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')

class FuriaBot:
    def __init__(self):
        self.matches_cache = {}
        self.last_cache_update = None

    def get_main_menu_keyboard(self):
        """Retorna o teclado do menu principal"""
        keyboard = [
            [InlineKeyboardButton("ℹ️ Informações sobre o Time", callback_data="team_info")],
            [InlineKeyboardButton("📺 Lives de CS na Twitch", callback_data="twitch_lives")],
            [InlineKeyboardButton("📱 Canais da FURIA", callback_data="furia_channels")],
            [InlineKeyboardButton("🛍️ Lojinha da FURIA", callback_data="furia_shop")]
        ]
        return InlineKeyboardMarkup(keyboard)

    def get_team_info_keyboard(self):
        """Retorna o teclado do submenu de informações do time"""
        keyboard = [
            [InlineKeyboardButton("🎮 Próximos Jogos", callback_data="next_matches")],
            [InlineKeyboardButton("🏆 Últimos Resultados", callback_data="results")],
            [InlineKeyboardButton("📊 Ranking", callback_data="ranking")],
            [InlineKeyboardButton("👥 Elenco Atual", callback_data="roster")],
            [InlineKeyboardButton("⬅️ Voltar ao Menu Principal", callback_data="main_menu")]
        ]
        return InlineKeyboardMarkup(keyboard)

    def get_welcome_message(self):
        """Retorna a mensagem de boas-vindas"""
        return (
            "🐯 Bem-vindo ao FURIA Fan Bot!\n\n"
            "Seu assistente completo para acompanhar a FURIA!\n\n"
            "Escolha uma opção abaixo para começar:"
        )

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler para o comando /start"""
        await update.message.reply_text(
            self.get_welcome_message(),
            reply_markup=self.get_main_menu_keyboard()
        )

    def get_back_button(self):
        """Retorna o botão de voltar"""
        keyboard = [[InlineKeyboardButton("⬅️ Voltar ao Menu Principal", callback_data="main_menu")]]
        return InlineKeyboardMarkup(keyboard)

    def get_back_to_team_info_button(self):
        """Retorna o botão de voltar para o menu de informações do time"""
        keyboard = [[InlineKeyboardButton("⬅️ Voltar às Informações do Time", callback_data="team_info")]]
        return InlineKeyboardMarkup(keyboard)

    async def show_main_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Mostra o menu principal"""
        await update.callback_query.message.edit_text(
            self.get_welcome_message(),
            reply_markup=self.get_main_menu_keyboard()
        )

    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler para todos os botões do bot"""
        query = update.callback_query
        await query.answer()

        if query.data == "main_menu":
            await self.show_main_menu(update, context)
            return

        if query.data == "team_info":
            message = (
                "ℹ️ Informações sobre a FURIA\n\n"
                "Selecione o que você quer saber sobre nosso time:"
            )
            await query.message.edit_text(
                message,
                reply_markup=self.get_team_info_keyboard()
            )
            return

        if query.data == "next_matches":
            # Simulando resposta de API
            matches = {
                "upcoming_matches": [
                    {
                        "opponent": "NAVI",
                        "event": "ESL Pro League Season 19",
                        "date": "2024-05-06 15:00",
                        "format": "BO3",
                        "tournament_prize": "$850,000"
                    },
                    {
                        "opponent": "Cloud9",
                        "event": "BLAST Premier Spring Finals",
                        "date": "2024-05-08 18:30",
                        "format": "BO3",
                        "tournament_prize": "$425,000"
                    }
                ]
            }

            message = "📅 Próximos Jogos da FURIA:\n\n"
            for match in matches["upcoming_matches"]:
                message += (
                    f"🆚 FURIA vs {match['opponent']}\n"
                    f"🏆 Torneio: {match['event']}\n"
                    f"💰 Premiação: {match['tournament_prize']}\n"
                    f"⏰ Data: {match['date']}\n"
                    f"📍 Formato: {match['format']}\n\n"
                )

            await query.message.edit_text(message, reply_markup=self.get_back_to_team_info_button())

        elif query.data == "ranking":
            # Simulando resposta de API
            ranking_data = {
                "hltv_ranking": {
                    "world_position": 12,
                    "points": 1250,
                    "region_position": 1,
                    "region": "Americas",
                    "ranking_changes": [
                        {"week": "Semana passada", "position": 14},
                        {"week": "Mês passado", "position": 16}
                    ],
                    "achievements": [
                        "Top 1 Brasil",
                        "Top 3 Americas",
                        "Qualified for Major 2024"
                    ]
                }
            }

            message = (
                "📊 Ranking Mundial CS2:\n\n"
                f"🌎 Posição Mundial: #{ranking_data['hltv_ranking']['world_position']}\n"
                f"📈 Pontos HLTV: {ranking_data['hltv_ranking']['points']}\n"
                f"🌎 #{ranking_data['hltv_ranking']['region_position']} {ranking_data['hltv_ranking']['region']}\n\n"
                "📈 Histórico:\n"
                f"• {ranking_data['hltv_ranking']['ranking_changes'][0]['week']}: #{ranking_data['hltv_ranking']['ranking_changes'][0]['position']}\n"
                f"• {ranking_data['hltv_ranking']['ranking_changes'][1]['week']}: #{ranking_data['hltv_ranking']['ranking_changes'][1]['position']}\n\n"
                "🏆 Conquistas:\n"
            )
            for achievement in ranking_data["hltv_ranking"]["achievements"]:
                message += f"• {achievement}\n"

            await query.message.edit_text(message, reply_markup=self.get_back_to_team_info_button())

        elif query.data == "results":
            # Simulando resposta de API
            results_data = {
                "recent_matches": [
                    {
                        "opponent": "Imperial",
                        "result": "2-0",
                        "event": "ESL Pro League",
                        "date": "2024-05-01",
                        "maps": ["Inferno (16-7)", "Mirage (16-12)"]
                    },
                    {
                        "opponent": "MIBR",
                        "result": "1-2",
                        "event": "BLAST Premier",
                        "date": "2024-04-28",
                        "maps": ["Ancient (16-13)", "Inferno (12-16)", "Overpass (14-16)"]
                    },
                    {
                        "opponent": "paiN",
                        "result": "2-1",
                        "event": "ESL Pro League",
                        "date": "2024-04-25",
                        "maps": ["Nuke (16-10)", "Vertigo (13-16)", "Mirage (16-14)"]
                    }
                ]
            }

            message = "🎮 Últimos Resultados:\n\n"
            for match in results_data["recent_matches"]:
                message += (
                    f"📅 {match['date']}\n"
                    f"🏆 {match['event']}\n"
                    f"FURIA {match['result']} {match['opponent']}\n"
                    "🗺️ Maps:\n"
                )
                for map_result in match['maps']:
                    message += f"• {map_result}\n"
                message += "\n"

            await query.message.edit_text(message, reply_markup=self.get_back_to_team_info_button())

        elif query.data == "roster":
            # Simulando resposta de API
            roster_data = {
                "players": [
                    {
                        "nickname": "KSCERATO",
                        "name": "Kaike Cerato",
                        "age": 24,
                        "role": "Rifler",
                        "nationality": "Brasil",
                        "joined_date": "2018-09-15"
                    },
                    {
                        "nickname": "yuurih",
                        "name": "Yuri Boian",
                        "age": 23,
                        "role": "Rifler",
                        "nationality": "Brasil",
                        "joined_date": "2017-11-08"
                    },
                    {
                        "nickname": "FalleN",
                        "name": "Gabriel Toledo",
                        "age": 33,
                        "role": "AWPer / IGL",
                        "nationality": "Brasil",
                        "joined_date": "2023-07-03"
                    },
                    {
                        "nickname": "molodoy",
                        "name": "Danil Golubenko",
                        "age": 21,
                        "role": "Entry Fragger",
                        "nationality": "Cazaquistão",
                        "joined_date": "2025-04-11"
                    },
                    {
                        "nickname": "YEKINDAR",
                        "name": "Mareks Gaļinskis",
                        "age": 25,
                        "role": "Stand-in",
                        "nationality": "Letônia",
                        "joined_date": "2025-04-22"
                    }
                ],
                "coach": {
                    "nickname": "sidde",
                    "name": "Sidnei Macedo",
                    "age": 34,
                    "nationality": "Brasil",
                    "joined_date": "2024-07-09"
                }
            }

            message = "👥 Elenco Atual FURIA CS2:\n\n"
            for player in roster_data["players"]:
                message += (
                    f"• {player['nickname']} - {player['name']}\n"
                    f"  Idade: {player['age']}\n"
                    f"  Função: {player['role']}\n"
                    f"  Na FURIA desde: {player['joined_date']}\n\n"
                )

            message += (
                "👨‍💼 Coach:\n"
                f"• {roster_data['coach']['nickname']} - {roster_data['coach']['name']}\n"
                f"  Idade: {roster_data['coach']['age']}\n"
                f"  Na FURIA desde: {roster_data['coach']['joined_date']}"
            )

            await query.message.edit_text(message, reply_markup=self.get_back_to_team_info_button())

        elif query.data == "twitch_lives":
            # Simulando resposta de API
            twitch_data = {
                "live_channels": [
                    {
                        "streamer": "gaules",
                        "title": "FURIA vs NAVI - ESL Pro League",
                        "viewers": 145000,
                        "language": "PT-BR",
                        "url": "twitch.tv/gaules"
                    },
                    {
                        "streamer": "ESL_CSGO",
                        "title": "FURIA vs NAVI - ESL Pro League",
                        "viewers": 89000,
                        "language": "EN",
                        "url": "twitch.tv/esl_csgo"
                    },
                    {
                        "streamer": "furiatv",
                        "title": "TREINO FURIA",
                        "viewers": 12000,
                        "language": "PT-BR",
                        "url": "twitch.tv/furiatv"
                    }
                ]
            }

            message = "📺 Lives de CS Relacionadas à FURIA:\n\n"
            for stream in twitch_data["live_channels"]:
                message += (
                    f"🎮 {stream['streamer']}\n"
                    f"📝 {stream['title']}\n"
                    f"👥 {stream['viewers']:,} viewers\n"
                    f"🌐 {stream['language']}\n"
                    f"🔗 {stream['url']}\n\n"
                )

            await query.message.edit_text(message, reply_markup=self.get_back_button())

        elif query.data == "furia_channels":
            # Simulando resposta de API
            channels_data = {"social_media": [
            {
                "platform": "Instagram",
                "handle": "@furiagg",
                "followers_count": "902K",
                "url": "instagram.com/furiagg"
            },
            {
                "platform": "Twitter",
                "handle": "@FURIA",
                "followers_count": "594K",
                "url": "twitter.com/furia"
            },
            {
                "platform": "YouTube",
                "handle": "FURIA",
                "followers_count": "64K",
                "url": "youtube.com/furiagg"
            },
            {
                "platform": "TikTok",
                "handle": "@furiagg",
                "followers_count": "97K",
                "url": "tiktok.com/@furiagg"
            },
            {
                "platform": "Twitch",
                "handle": "furiatv",
                "followers_count": "163K",
                "url": "twitch.tv/furiatv"
            }
        ]
            }

            message = "📱 Canais Oficiais da FURIA:\n\n"
            for channel in channels_data["social_media"]:
                message += (
                    f"📍 {channel['platform']}\n"
                    f"👤 {channel['handle']}\n"
                    f"👥 Seguidores: {channel['followers_count']}\n"
                    f"🔗 {channel['url']}\n\n"
                )

            await query.message.edit_text(message, reply_markup=self.get_back_button())

        elif query.data == "furia_shop":
            # Simulando resposta de API
            shop_data = {
                "featured_products": [
                    {
                        "name": "Moletom FURIA x Champion College Preto",
                        "price": "R$ 499,99",
                        "category": "Casual",
                        "available_sizes": ["P", "M", "G", "GG"],
                        "url": "https://www.furia.gg/produto/moletom-furia-x-champion-college-preto-150174",
                        "collection": "Champion"
                    },
                    {
                        "name": "Camiseta FURIA adidas Preta",
                        "price": "R$ 299,99",
                        "category": "Casual",
                        "available_sizes": ["P", "M", "G", "GG"],
                        "url": "https://www.furia.gg/produto/camiseta-furia-adidas-preta-150263",
                        "collection": "Adidas"
                    },
                    {
                        "name": "Calça FURIA Future is Black Preta",
                        "price": "R$ 279,90",
                        "category": "Casual",
                        "available_sizes": ["P", "M", "G", "GG"],
                        "url": "https://www.furia.gg/produto/calca-furia-future-is-black-preta-150143",
                        "collection": "Future is Black"
                    }
                ],
                "promo_code": "FURIABOT10"
            }

            message = (
                "🛍️ Lojinha Oficial da FURIA\n\n"
                "🔥 Produtos em Destaque:\n\n"
            )

            for product in shop_data["featured_products"]:
                message += (
                    f"📌 {product['name']}\n"
                    f"💰 {product['price']}\n"
                    f"📁 Collection: {product['collection']}\n"
                    f"📏 Tamanhos: {', '.join(product['available_sizes'])}\n"
                    f"🔗 {product['url']}\n\n"
                )

            message += (
                "🎉 Use o cupom de desconto:\n"
                f"🏷️ {shop_data['promo_code']} - 10% OFF"
            )

            await query.message.edit_text(message, reply_markup=self.get_back_button())

def run_bot():
    """Função para iniciar o bot"""
    logger.info("Iniciando o bot...")

    # Criar o bot e adicionar handlers
    bot = FuriaBot()
    application = Application.builder().token(TOKEN).build()

    # Adicionar handlers
    application.add_handler(CommandHandler("start", bot.start_command))
    application.add_handler(CallbackQueryHandler(bot.button_handler))

    # Iniciar o bot
    logger.info("Bot iniciado. Pressione Ctrl+C para parar.")
    application.run_polling(poll_interval=1.0, timeout=30)

if __name__ == '__main__':
    try:
        run_bot()
    except Exception as e:
        logger.error(f"Erro ao executar o bot: {e}")