class Avatars_by_name:
  def __init__(self):
    self.avatars={
      "Wan":"Wan was the first avatar",
      "Szeto":"Second Avatar Known",
      "Yangchen":"Third Avatar Known",
      "Kuruk":"Fourth Avatar Known",
      "Kyoshi":"Fifth Avatar Known",
      "Roku":"Sixth Avatar Known",
      "Aang":"Seventh Avatar Known",
      "Korra":"Eighth Avatar Known"
    }
  def get_av_name(self):
    return self.avatars
avatar_name=Avatars_by_name().get_av_name()
class Avatars_by_number:
  def __init__(self):
    self.avatars={
      1:"Wan",
      2:"Szeto",
      3:"Yangchen",
      4:"Kuruk",
      5:"Kyoshi",
      6:"Roku",
      7:"Aang",
      8:"Korra"
    }
  def get_av_number(self):
    return self.avatars
avatar_number=Avatars_by_number().get_av_number()