import cloudinary
import cloudinary.uploader


def upload_vectorstore():
    cloudinary.config(
        cloud_name='dcqokkmou',
        api_key='964177694921314',
        api_secret='Py_putww367rN_DTw_b7C7uR39g',
        secure=True
    )
    name = 'fghgsfd'
    public_path = f"C:\\Users\\user\\Desktop\\Тестове завдання веб-програміст.docx"
    # cloudinary.
    # file_name = public_name + "_" + str(current_user.username)
    r = cloudinary.uploader.upload(public_path, public_id=f'PhotoShare/{name}', overwrite=True)
    # src_url = cloudinary.CloudinaryImage(f'PhotoShare/{name}') \
    #     .build_url(version=r.get('version'))
    print(r)


upload_vectorstore()