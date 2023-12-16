import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from text_clf import clf, bran, big_model


def write_message(sender, message):
    authorize.method('messages.send', {'user_id': sender, 'message': message, 'random_id': get_random_id()})


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    token = "vk1.a.eAH3gNa4IyKUj20yydBX0iE9lAfBfBjTTP3zD59LhQlwO-UBu4KADo1MtcQWiMsNqVpzXxQOhcKYRPreBJHvQNFUIvdW8JUu2bxoJUOnda5KNRLTApijbeCw4ZvaA9If4rFB1FcO6e86rucpspj2RwY-atIcc27cfjxRZPaHPLIZFMNE9xIXecskNr17VyCvsYplquMKr1mlUP02Ks1tog"
    authorize = vk_api.VkApi(token=token)
    longpoll = VkLongPoll(authorize)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            reseived_message = event.text
            sender = event.user_id

            if bran(reseived_message):
                write_message(sender, "Извините, но я не могу обработать оскорбительные\
                или нецензурные выражения. Если у вас есть вопрос или запрос, сформулируйте его в уважительной форме,\
                и я постараюсь вам помочь.")
            else:
                if clf(reseived_message):
                    answer = big_model(reseived_message)
                    if "!" in answer:
                        write_message(sender, answer[:1 + answer.find(".")])
                    else:
                        k = answer.find(".", answer.find(".") + 1)
                        write_message(sender, answer[:k + 1])
                else:
                    write_message(sender, "Прошу прощения,\
                    но ваш вопрос касается темы, которую я не могу обсудить.\
                    Если у вас есть другие вопросы или темы для обсуждения, пожалуйста, напишите их,\
                    и я постараюсь вам помочь.")
