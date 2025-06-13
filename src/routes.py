# -*- coding: utf-8 -*-
from src.resources.auth_resource import AuthResource, LogoutResource, ResetPasswordResource, CheckEmailResource, \
    SystemResource, ErrorResource, WebViewResource, UpdatePasswordResource
from src.resources.user_resource import UserResource, RegisterResource, UpdateMeResource, WaterResource, \
    ProfileResource, DieticianResource, ApprovalsResource, ClientResource, ApproveResource, PauseResource, \
    StatusResource, SportResource, ClientItemResource, NotesResource, WeightResource, ClientProfileResource, \
    TrackingResource, RenewalsResource, ProfileUpdateResource, MonthlyResource, WeightsResource, UpdateWeightResource, \
    DeleteWeightResource
from src.resources.diet_resource import PlanResource, HomeResource, MyPlansResource, MyPlanResource, DietResource, \
    ClientPlansResource, DeleteDietResource
from src.resources.timezones_resource import TimezonesResource
from src.resources.answer_resource import AnswerResource, NewAnswerResource, DetailAnswerResource, \
    UpdateAnswerResource, DeleteAnswerResource
from src.resources.message_resource import SendMessageResource, DeleteMessageResource, UnReadMessageResource, \
    MyMessageResource, MediaMessageResource, MultipleMessageResource, InboxResource, InboxArchiveResource, \
    MessageResource, MediaResource, ArchiveMessageResource
from src.resources.file_resource import FileResource


def routes(api):
    api.add_resource(AuthResource, "/login")
    api.add_resource(LogoutResource, "/logout")
    api.add_resource(ResetPasswordResource, "/reset-password")
    api.add_resource(UpdatePasswordResource, "/update-password")
    api.add_resource(CheckEmailResource, "/check-email")
    api.add_resource(RegisterResource, "/register")
    api.add_resource(UserResource, "/user")
    api.add_resource(TimezonesResource, "/timezones")
    api.add_resource(SystemResource, "/system")
    api.add_resource(ErrorResource, "/error")
    api.add_resource(WebViewResource, "/web-view")
    api.add_resource(PlanResource, "/plan")
    api.add_resource(UpdateMeResource, "/update-me")
    api.add_resource(WaterResource, "/water")
    api.add_resource(SportResource, "/sport")
    api.add_resource(HomeResource, "/home")
    api.add_resource(ProfileResource, "/profile")
    api.add_resource(MyPlansResource, "/my-plans")
    api.add_resource(MyPlanResource, "/my-plan")
    api.add_resource(DieticianResource, "/dieticians")
    api.add_resource(ApprovalsResource, "/approvals")
    api.add_resource(ClientResource, "/clients")
    api.add_resource(ClientItemResource, "/client/<int:cid>")
    api.add_resource(ApproveResource, "/approve")
    api.add_resource(PauseResource, "/pause")
    api.add_resource(StatusResource, "/status")
    api.add_resource(NotesResource, "/note-update")
    api.add_resource(WeightResource, "/log-weight")
    api.add_resource(DietResource, "/diet")
    api.add_resource(ClientProfileResource, "/client-profile")
    api.add_resource(ClientPlansResource, "/client-plans")
    api.add_resource(TrackingResource, "/tracking")
    api.add_resource(RenewalsResource, "/renewals")
    api.add_resource(ProfileUpdateResource, "/profile-update")
    api.add_resource(MonthlyResource, "/monthly")
    api.add_resource(DeleteDietResource, "/delete-diet")
    api.add_resource(WeightsResource, "/weights/<int:wid>")
    api.add_resource(UpdateWeightResource, "/update-weight")
    api.add_resource(DeleteWeightResource, "/delete-weight")
    api.add_resource(AnswerResource, "/answers")
    api.add_resource(NewAnswerResource, "/answers/new")
    api.add_resource(DetailAnswerResource, "/answers/detail")
    api.add_resource(UpdateAnswerResource, "/answers/update")
    api.add_resource(DeleteAnswerResource, "/answers/delete")
    # Messages
    api.add_resource(SendMessageResource, "/message")
    api.add_resource(DeleteMessageResource, "/delete-message")
    api.add_resource(UnReadMessageResource, "/unread")
    api.add_resource(MyMessageResource, "/my-messages")
    api.add_resource(MediaMessageResource, "/my-media")
    api.add_resource(MultipleMessageResource, "/multiple-message")
    api.add_resource(InboxResource, "/inbox")
    api.add_resource(InboxArchiveResource, "/inbox-archive")
    api.add_resource(MessageResource, "/messages")
    api.add_resource(MediaResource, "/medias")
    api.add_resource(FileResource, "/file/S3/<string:file_name>")
    api.add_resource(ArchiveMessageResource, "/archive-user")
