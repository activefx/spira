require File.dirname(__FILE__) + "/spec_helper.rb"
# testing out default vocabularies

describe 'default vocabularies' do

  before :all do
    @bubble_repo = RDF::Repository.new
    Spira.add_repository(:default, @bubble_repo)

  end

  before :each do
    @vocabulary = RDF::URI.new('http://example.org/vocabulary/')
  end

  context "defining classes" do
    it "should allow a property without a predicate if there is a default vocabulary" do
      lambda {
        class VocabTestX
          include Spira::Resource
          default_vocabulary RDF::URI.new('http://example.org/vocabulary/')
          property :test
        end
      }.should_not raise_error
    end

    it "should raise a ResourceDeclarationError to set a property without a default vocabulary" do
      lambda {
        class VocabTestY
          include Spira::Resource
          property :test
        end
      }.should raise_error Spira::ResourceDeclarationError
    end

    it "should raise a ResourceDelcarationError to set a predicate without a default vocabulary that is not an RDF::URI" do
      lambda {
        class VocabTestY
          include Spira::Resource
          property :test, :predicate => "http://example.org/test"
        end
      }.should raise_error Spira::ResourceDeclarationError
    end
  end

  context "using classes with a default vocabulary" do

    before :all do
      class ::Bubble
        include Spira::Resource

        default_vocabulary RDF::URI.new 'http://example.org/vocab/'

        base_uri "http://example.org/bubbles/"
        property :year, :type => Integer
        property :name
        property :title, :predicate => DC.title, :type => String
      end
      class ::DefaultVocabVocab < ::RDF::Vocabulary('http://example.org/test#') ; end
      class ::HashVocabTest
        include Spira::Resource
        default_vocabulary DefaultVocabVocab
        base_uri "http://example.org/testing/"
        property :name
      end
      class ::DefaultColonVocab < ::RDF::Vocabulary('http://example.org/test:') ; end
      class ::ColonVocabTest
        include Spira::Resource
        default_vocabulary DefaultColonVocab
        base_uri "http://example.org/testing/"
        property :name
      end
      class ::DefaultEncodedSlashVocab < ::RDF::Vocabulary('http://example.org/test-2F') ; end
      class ::EncodedSlashVocabTest
        include Spira::Resource
        default_vocabulary DefaultEncodedSlashVocab
        base_uri "http://example.org/testing/"
        property :name
      end
      class ::DefaultEncodedColonVocab < ::RDF::Vocabulary('http://example.org/test-3A') ; end
      class ::EncodedColonVocabTest
        include Spira::Resource
        default_vocabulary DefaultEncodedColonVocab
        base_uri "http://example.org/testing/"
        property :name
      end
      class ::DefaultEncodedHashVocab < ::RDF::Vocabulary('http://example.org/test-23') ; end
      class ::EncodedHashVocabTest
        include Spira::Resource
        default_vocabulary DefaultEncodedHashVocab
        base_uri "http://example.org/testing/"
        property :name
      end
    end

    before :each do
      @year = RDF::URI.new 'http://example.org/vocab/year'
      @name = RDF::URI.new 'http://example.org/vocab/name'
    end

    it "should do non-default sets and gets normally" do
      bubble = Bubble.for 'tulips'
      bubble.year = 1500
      bubble.title = "Holland tulip"
      bubble.save!

      bubble.title.should == "Holland tulip"
      bubble.should have_predicate RDF::DC.title
    end
    it "should create a predicate for a given property" do
      bubble = Bubble.for 'dotcom'
      bubble.year = 2000
      bubble.name = 'Dot-com boom'

      bubble.save!
      bubble.should have_predicate @year
      bubble.should have_predicate @name
    end

    context "that ends in a hash seperator" do
      before :each do
        @name = RDF::URI("http://example.org/test#name")
      end

      it "should correctly not append a slash" do
        test = HashVocabTest.for('test1')
        test.name = "test1"
        test.save!
        test.should have_predicate @name
      end
    end

    context "that ends in a colon seperator" do
      before :each do
        @name = RDF::URI("http://example.org/test:name")
      end

      it "should correctly not append a slash" do
        test = ColonVocabTest.for('test2')
        test.name = "test2"
        test.save!
        test.should have_predicate @name
      end
    end

    context "that ends in an encoded slash seperator" do
      before :each do
        @name = RDF::URI("http://example.org/test-2Fname")
      end

      it "should correctly not append a slash" do
        test = EncodedSlashVocabTest.for('test3')
        test.name = "test3"
        test.save!
        test.should have_predicate @name
      end
    end

    context "that ends in an encoded colon seperator" do
      before :each do
        @name = RDF::URI("http://example.org/test-3Aname")
      end

      it "should correctly not append a slash" do
        test = EncodedColonVocabTest.for('test4')
        test.name = "test4"
        test.save!
        test.should have_predicate @name
      end
    end

    context "that ends in an encoded hash seperator" do
      before :each do
        @name = RDF::URI("http://example.org/test-23name")
      end

      it "should correctly not append a slash" do
        test = EncodedHashVocabTest.for('test5')
        test.name = "test5"
        test.save!
        test.should have_predicate @name
      end
    end

  end



end

