from flask import Flask, Blueprint
from flask_cors import CORS
from .config import config_by_name
from flask_restful import Api
from flask_jwt_extended import JWTManager
from main.controller.user_auth_controller import UserRegistrationController, UserLoginController , UserLogoutController
from main.controller.seller_auth_controller import SellerRegisterController, SellerLoginController, SellerLogoutController
from main.controller.shop_detail_controller import SellerContactController, SellerAddressController, SellerCategoryController, SellerProductController,SellerEmailController,SellerLocationController,SellerOwnerNameController,SellerActiveTimeController,SellerShopNameController,SellerDisplayNameController,OpenShopController,CloseShopController, SellerEarningController, SellerCouponsController
from main.controller.offer_controller import SellerOfferController, OfferController, RedeemController, SellerRedeemController
from main.controller.category_controller import CategoryController, ShopByCategoryController, OfferByCategoryController, OfferByShopController
from main.controller.history_controller import SellerHistoryController, CustomerHistoryController, CustomerPointsController
from main.controller.credentials_controller import SellerCredentialController, UserCredentialController
from main.controller.cart_controller import CartService
from main.controller.indexcontroller import IndexController
from main.controller.seller_image_controller import SellerImageController, SellerImageFromEmailController
from main.controller.admin_controller import AdminController, AdminPermissionController, AdminLoginController, ShopPermissionController



def create_app(config_name):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config_by_name[config_name])
    jwt = JWTManager(app)
    CORS(app)
    api_blueprint = Blueprint('api',__name__)
    api = Api(api_blueprint)

    api.add_resource(IndexController,'/')
    ## user authentication and registration
    api.add_resource(UserRegistrationController,'/register')
    api.add_resource(UserLoginController,'/login')
    api.add_resource(UserLogoutController,'/logout')
   
    ## seller authentication and registration
    api.add_resource(SellerRegisterController,'/seller/register')
    api.add_resource(SellerLogoutController,'/seller/logout')
    api.add_resource(SellerLoginController,'/seller/login')
   
    ##seller details 
    api.add_resource(SellerContactController,'/seller/update_contact')
    api.add_resource(SellerAddressController,'/seller/update_address')

    api.add_resource(SellerCategoryController,'/seller/category')
    api.add_resource(SellerProductController,'/seller/product')
    
    api.add_resource(SellerEmailController,'/seller/update_email')
    api.add_resource(SellerLocationController,'/seller/update_location')
    api.add_resource(SellerActiveTimeController,'/seller/update_active_time')
    api.add_resource(SellerShopNameController,'/seller/update_shop_name')
    api.add_resource(SellerOwnerNameController,'/seller/update_owner_name')
    api.add_resource(SellerDisplayNameController,'/seller/update_display_name')
    api.add_resource(OpenShopController,'/seller/open_shop')
    api.add_resource(CloseShopController,'/seller/close_shop')
    api.add_resource(SellerEarningController, '/seller/earning')
    api.add_resource(SellerCouponsController, '/seller/get_coupons')
    
    ## add and remove offer (by seller)
    api.add_resource(SellerOfferController,'/seller/offer')
    api.add_resource(OfferController, '/get_all_offers')

    ## redeem apis
    api.add_resource(RedeemController,'/redeem')
    api.add_resource(SellerRedeemController,'/seller/redeem')

    ## category api
    api.add_resource(CategoryController, '/categories')
    api.add_resource(ShopByCategoryController, '/get_shops/<category>')

    ## get offers by category
    api.add_resource(OfferByCategoryController, '/get_offers_by_category/<category>')

    ## get offers by shop_name
    api.add_resource(OfferByShopController, '/get_offers_by_shop/<shop_name>')

    ## history api
    api.add_resource(SellerHistoryController, '/seller/history')
    api.add_resource(CustomerHistoryController, '/history')
    api.add_resource(CustomerPointsController, '/credit')


    ## Credential apis
    api.add_resource(SellerCredentialController, '/seller/cred')
    api.add_resource(UserCredentialController, '/cred')

    ##cart api
    api.add_resource(CartService,'/cart')
    
    ## seller image api
    api.add_resource(SellerImageController, '/seller/image','/seller/image/<email>')
    api.add_resource(SellerImageFromEmailController,'/seller_image/<email>')

    ## admin 
    api.add_resource(AdminController, '/admin')
    api.add_resource(AdminPermissionController, '/admin/permission')
    api.add_resource(AdminLoginController, '/admin/login')
    api.add_resource(ShopPermissionController, '/admin/shop')

    app.register_blueprint(api_blueprint)


    return app