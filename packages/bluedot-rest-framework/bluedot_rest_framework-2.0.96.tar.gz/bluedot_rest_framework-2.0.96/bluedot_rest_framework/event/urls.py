from rest_framework.routers import DefaultRouter
from bluedot_rest_framework import import_string

EventView = import_string('EVENT.views')
EventQuestionView = import_string('EVENT.question.views')
EventQuestionUserView = import_string('EVENT.question.user_views')
EventScheduleView = import_string('EVENT.schedule.views')
EventSpeakerView = import_string('EVENT.speaker.views')
EventDataDownloadView = import_string('EVENT.data_download.views')
EventRegisterView = import_string('EVENT.register.views')
EventChatView = import_string('EVENT.chat.views')
EventConfigurationView = import_string('EVENT.configuration.views')
EventCommentView = import_string('EVENT.comment.views')
EventVoteView = import_string('EVENT.vote.views')
EventVoteUserView = import_string('EVENT.vote.user_views')
EventVenueView = import_string('EVENT.venue.views')


router = DefaultRouter(trailing_slash=False)
router.register(r'event/venue', EventVenueView,
                basename='event-venue')
router.register(r'event/vote/user', EventVoteUserView,
                basename='event-vote-user')
router.register(r'event/vote', EventVoteView,
                basename='event-vote')
router.register(r'event/configuration', EventConfigurationView,
                basename='event-configuration')
router.register(r'event/question/user', EventQuestionUserView,
                basename='event-question-user')
router.register(r'event/chat', EventChatView,
                basename='event-chat')
router.register(r'event/comments', EventCommentView,
                basename='event-comments')
router.register(r'event/register', EventRegisterView,
                basename='event-register')
router.register(r'event/question', EventQuestionView,
                basename='event-question')
router.register(r'event/data-download', EventDataDownloadView,
                basename='event-data-download')
router.register(r'event/speaker', EventSpeakerView,
                basename='event-speaker')
router.register(r'event/schedule', EventScheduleView,
                basename='event-schedule')
router.register(r'event', EventView,
                basename='event')

urlpatterns = router.urls
