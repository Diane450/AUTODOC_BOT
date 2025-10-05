class BotUtils:
    
    def get_text_for_output_type(self, output_type):
            
            if output_type == "zip":
                return "Ваши документы будут присланы в ZIP архиве"
            return "Ваши документы будут присланы в едином файле"