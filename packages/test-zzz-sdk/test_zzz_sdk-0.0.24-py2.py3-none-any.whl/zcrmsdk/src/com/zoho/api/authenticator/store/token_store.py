try:
    from abc import ABC, abstractmethod
    # from zcrmsdk.src.com.zoho.api.authenticator import Token
    # from zcrmsdk.src.com.zoho.crm.api import UserSignature

except Exception as e:
    from abc import ABC, abstractmethod
    # from ..token import Token
    # from ....crm.api import UserSignature


class TokenStore(ABC):

    """
    This class is to store user token details.
    """

    @abstractmethod
    def get_token(self, user, token):

        """
        The method to get user token details.

        Parameters:
            user (UserSignature) : A UserSignature class instance.
            token (Token) : A Token class instance.

        Returns:
            Token : A Token class instance representing the user token details.
        """

        pass

    @abstractmethod
    def save_token(self, user, token):

        """
        The method to store user token details.

        Parameters:
            user (UserSignature) : A UserSignature class instance.
            token (Token) : A Token class instance.

        Returns:
            Token : A Token class instance representing the user token details.
        """

        pass

    @abstractmethod
    def delete_token(self, token):

        """
        The method to delete user token details.

        Parameters:
            token (Token) : A Token class instance.

        Returns:
            Token : A Token class instance representing the user token details.
        """

        pass

    @abstractmethod
    def get_tokens(self):

        """
        The method to retrieve all the stored tokens.

        Returns:
            list : A List of Token instances
        """

        pass

    @abstractmethod
    def delete_tokens(self):

        """
        The method to delete all the stored tokens.
        """

        pass
