from ..core import Core
from ..utils.exchangeversion import ExchangeVersion
from ..utils.exceptions import DeleteTypeError


class DeleteItem(Core):
    '''Deletes items (typically email messages) from a users mailboxes.

    Examples:
        
    To use any service class you must provide a UserConfiguration object first.
    Like all service classes, you can access formatted properties from the EWS endpoint using the `response` property.

    If you want to move a single message to the `Deleted Items` folder then provide a string value of the message ID.
    The default `delete_type` is to move a message to the `Deleted Items` folder.

    ```python
    userconfig = UserConfiguration(
        'first.last@company.com',
        'mypassword123'
    )
    messageId = 'AAMkAGZjOTlkOWExLTM2MDEtNGI3MS04ZDJiLTllNzgwNDQxMThmMABGAAAAAABdQG8UG7qjTKf0wCVbqLyMBwC6DuFzUH4qRojG/OZVoLCfAAAAAAEMAAC6DuFzUH4qRojG/OZVoLCfAAAu4Y9UAAA='
    deleteItem = DeleteItem(userconfig).run(message_id)
    ```

    If you want to HardDelete a single message then provide a string value of the message ID and specify the `delete_type` as `HardDelete`:

    ```python
    from pyews import UserConfiguration
    from pyews import DeleteItem

    userconfig = UserConfiguration(
        'first.last@company.com',
        'mypassword123'
    )

    messageId = 'AAMkAGZjOTlkOWExLTM2MDEtNGI3MS04ZDJiLTllNzgwNDQxMThmMABGAAAAAABdQG8UG7qjTKf0wCVbqLyMBwC6DuFzUH4qRojG/OZVoLCfAAAAAAEMAAC6DuFzUH4qRojG/OZVoLCfAAAu4Y9UAAA='
    deleteItem = DeleteItem(userConfig).run(message_id, delete_type='HardDelete')
    ```

    Args:
        messageId (list or str): An email MessageId to delete
        userconfiguration (UserConfiguration): A UserConfiguration object created using the UserConfiguration class
        delete_type (str, optional): Defaults to MoveToDeletedItems. Specify the DeleteType.  Available options are ['HardDelete', 'SoftDelete', 'MoveToDeletedItems']

    Raises:
        SoapAccessDeniedError: Access is denied when attempting to use Exchange Web Services endpoint
        SoapResponseHasError: An error occurred when parsing the SOAP response
        ObjectType: An incorrect object type has been used
    '''

    DELETE_TYPES = ['HardDelete', 'SoftDelete', 'MoveToDeletedItems']

    def __init__(self, userconfiguration):
        super(DeleteItem, self).__init__(userconfiguration)

    def __parse_response(self, value):
        '''Creates and sets a response object

        Args:
            value (str): The raw response from a SOAP request
        '''
        return_list = []
        if value.find('ResponseCode').string != 'NoError':
            for item in value.find_all('DeleteItemResponseMessage'):
                return_list.append({
                    'MessageText': item.MessageText.string,
                    'ResponseCode': item.ResponseCode.string,
                    'DescriptiveLinkKey': item.DescriptiveLinkKey.string
                })
        else:
            return_list.append({
                'MessageText': 'Successfull'
            })
        return return_list

    def run(self, message_id, delete_type=DELETE_TYPES[2]):
        if delete_type in self.DELETE_TYPES:
            self.delete_type = delete_type
        else:
            raise DeleteTypeError('You must provide one of the following delete types: {}'.format(self.DELETE_TYPES))
        self.raw_xml = self.invoke(self.soap(message_id))
        return self.__parse_response(self.raw_xml)

    def soap(self, item):
        '''Creates the SOAP XML message body

        Args:
            item (str or list): A single or list of message ids to delete

        Returns:
            str: Returns the SOAP XML request body
        '''
        if self.userconfiguration.impersonation:
            impersonation_header = self.userconfiguration.impersonation.header
        else:
            impersonation_header = ''

        delete_item_soap_element = self.__delete_item_soap_string(item)
        return '''<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types"
               xmlns:m="http://schemas.microsoft.com/exchange/services/2006/messages">
   <soap:Header>
      <t:RequestServerVersion Version="{version}" />
      {header}
   </soap:Header>
   <soap:Body >
    <DeleteItem DeleteType="{type}" xmlns="http://schemas.microsoft.com/exchange/services/2006/messages">
      <ItemIds>
        {soap_element}
      </ItemIds>
    </DeleteItem>
  </soap:Body>
</soap:Envelope>'''.format(
    version=self.userconfiguration.exchangeVersion, 
    header=impersonation_header, 
    type=self.delete_type, 
    soap_element=delete_item_soap_element
    )

    def __delete_item_soap_string(self, item):
        '''Creates a ItemId XML element from a single or list of items

        Returns:
            str: Returns the ItemId SOAP XML element(s)
        '''
        item_soap_string = ''
        if isinstance(item, list):
            for i in item:
                item_soap_string += '''<t:ItemId Id="{}"/>'''.format(i)
        else:
            item_soap_string = '''<t:ItemId Id="{}"/>'''.format(item)
        return item_soap_string
