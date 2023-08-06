from bergen.types.model import  ArnheimModelManager

class RepresentationManager(ArnheimModelManager):

    def from_xarray(self, array, compute=True, **kwargs):
        instance = self.create(**kwargs)
        instance.save_array(array, compute=compute)
        print(instance)
        instance = self.update(id=instance.id, **kwargs)
        return instance